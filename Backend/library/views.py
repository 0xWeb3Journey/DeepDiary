from datetime import datetime, timedelta

from celery.result import AsyncResult
from django.db.models import Count, Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from rest_framework.decorators import action
from rest_framework.response import Response

from deep_diary.config import wallet_info
from face.views import get_all_fts
from library.models import Img, ImgCategory, Mcs
from library.pagination import GalleryPageNumberPagination
from library.serializers import ImgSerializer, ImgDetailSerializer, ImgCategorySerializer, McsSerializer
from library.task import save_img_info, upload_img_to_mcs
from library.task import send_email

from mycelery.library.tasks import send_sms
from mycelery.main import app
from utils.mcs_storage import upload_file_pay, approve_usdc


class ImgCategoryViewSet(viewsets.ModelViewSet):
    queryset = ImgCategory.objects.all()
    serializer_class = ImgCategorySerializer


class ImgViewSet(viewsets.ModelViewSet):
    # queryset = Img.objects.all().distinct()
    queryset = Img.objects.annotate(Count('faces')).order_by('-id')
    # print(queryset)
    # queryset = Img.objects.filter(faces__id=44)
    serializer_class = ImgSerializer
    # permission_classes = (AllowAny,)
    pagination_class = GalleryPageNumberPagination  # could disp the filter button in the web
    # 第一种方法
    # filter_class = ImgFilter  # 过滤类

    # 第二种方法
    # DjangoFilterBackend  # 精准过滤，字段用filterset_fields定义
    # filters.SearchFilter  # 模糊搜索，字段用search_fields
    # filters.OrderingFilter  # 排序规则字段定义
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]  # 模糊过滤，注意的是，这里的url参数名变成了?search=搜索内容
    # filterset_fields = ['user__username', 'tags__name', 'year', 'month', 'day']
    filterset_fields = {
        'mcs__file_upload_id': ['gt', 'lt', 'exact'],  # 是否存在这个字段
        'faces__name': ['icontains'],  # 大于等于，小于等于，包含, 对于外键,可以需要使用双下划线指定具体字段
        'faces__id': ['gte', 'lte', 'contains'],  # 大于等于，小于等于，包含, 对于外键,可以需要使用双下划线指定具体字段
        'year': ['gte', 'lte', 'contains'],  # 大于等于，小于等于，包含
        'month': ['gte', 'lte', 'contains'],  # 大于等于，小于等于，包含
        'day': ['gte', 'lte', 'contains'],  # 大于等于，小于等于，包含
        'filename': ['icontains'],  # 模糊搜索
        'tags__name': ['icontains'],  # 模糊搜索
    }
    search_fields = ['user__username', 'tags__name', 'year', 'month', 'day']
    ordering_fields = ['tags__name']  # 这里的字段，需要总上面定义字段中选择

    def perform_create(self, serializer):
        print(f"INFO:{self.request.user}")
        instance = serializer.save(user=self.request.user)
        print(f'INFO: start perform_create........{instance.src}')
        save_img_info.delay(instance)
        upload_img_to_mcs.delay(instance)

        # w3_api = approve_usdc(wallet_info)

    def perform_update(self, serializer):  # 应该在调用的模型中添加
        # print(f'图片更新：{self.request.data}')
        instance = serializer.save()  # ProcessedImageField, 也就是ImageField的实例对象
        print(f'INFO: start perform_update........')

        # print(f"INFO: instance.src: {instance.src}")
        # print(f"INFO: instance.src.name: {instance.src.name}")
        # print(f"INFO: instance.src__filename: {os.path.basename(instance.src.name)}")
        # print(f"INFO: instance.src__filetype: {os.path.splitext(instance.src.name)[-1]}")  # 获取带点文件后缀
        # print(f"INFO: instance.src__filetype: {instance.src.name.split('.')[-1]}")  # 获取不带点文件后缀

        # print(f"INFO: instance.src.path: {instance.src.path}")
        # print(f"INFO: instance.src.url: {instance.src.url}")
        # print(f"INFO: instance.src.size: {instance.src.size}")
        # print(f"INFO: instance.src.width: {instance.src.width}")
        # print(f"INFO: instance.src.height: {instance.src.height}")
        # print(f"INFO: instance.src.storage: {instance.src.storage}")
        # print(f"INFO: instance.src.tell: {instance.src.tell}")
        # print(f"INFO: instance.src.field: {instance.src.field}")
        # print(f"INFO: instance.src.file: {instance.src.file}")
        # print(f"INFO: instance.src.file.name: {instance.src.file.name}")
        # print(f"INFO: instance.src.fileno: {instance.src.fileno}")
        # print(f"INFO: instance.src.flush: {instance.src.flush}")
        # print(f"INFO: instance.src.isatty: {instance.src.isatty}")

        # print(type(instance))
        # print(type(instance.tags))  # 获取这个实例的类型
        # print('----image attr----')
        # print(dir(instance.src))  # 获取这个实例的属性
        # print('----image.path attr----')
        # print(dir(instance.src.path))
        # print('----image.storage attr----')
        # print(dir(instance.src.storage))

        if 'tags' in self.request.data:
            # print(*self.request.data['tags'].split(','))
            instance.tags.set(self.request.data['tags'].split(','))

    def get_serializer_class(self):
        if self.action == 'list':
            return ImgSerializer
        else:
            return ImgDetailSerializer

    @action(detail=True, methods=['get'])  # 在详情中才能使用这个自定义动作
    def info(self, request, pk=None):  # 当detail=True 的时候，需要指定第三个参数，如果未指定look_up, 默认值为pk，如果指定，该值为loop_up的值
        img = self.get_object()  # 获取详情的实例对象
        print(f'INFO pk: {pk}')
        print(f'INFO img: {type(img)}')
        print(f'INFO img: {img.id}')
        # print(f'INFO request: {dir(request)}')

        # 上传图片后，直接通过信号机制，进行人脸识别保存
        # app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        # app.prepare(ctx_id=0, det_size=(640, 640))
        # # img = ins_get_image('t1',to_rgb=True)   # 官方提供的路径
        #
        # image_path = img.image.path
        # req_img = cv.imread(image_path)  # 自己用openCV进行读取
        # faces = app.get(req_img)
        # save_faces(img.id, image_path, faces)

        # serializer = ImgSerializer(img, many=False, context={'request': request})  # 不报错
        # serializer = ImgSerializer(img, many=False)  # 报错
        serializer = self.get_serializer(img)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])  # 在详情中才能使用这个自定义动作
    def info(self, request, pk=None):
        queryset = Img.objects.annotate(Count('faces'))
        serializer_class = ImgSerializer
        serializer = self.get_serializer(queryset[0])
        return Response({"data":"demo"})

    @action(detail=True, methods=['get'])  # 在详情中才能使用这个自定义动作
    def check_mcs(self, request, pk=None):
        print('---------------------------------------checking mcs')
        names, all_fts = get_all_fts()
        print(names)
        # result = send_email.delay('blue')
        # # result = send_sms.delay('111111')
        # async_result = AsyncResult(id=result.id, app=app)
        # if async_result.successful():
        #     result = async_result.get()
        #     print(result)
        #     # result.forget() # 将结果删除
        # elif async_result.failed():
        #     print('执行失败')
        # elif async_result.status == 'PENDING':
        #     print('任务等待中被执行')
        # elif async_result.status == 'RETRY':
        #     print('任务异常后正在重试')
        # elif async_result.status == 'STARTED':
        #     print('任务已经开始被执行')
        # else:
        #     print('无法识别错误')

        ################################# 定时任务

        # ctime = datetime.now()
        # # 默认用utc时间
        # utc_ctime = datetime.utcfromtimestamp(ctime.timestamp())
        # time_delay = timedelta(seconds=5)
        # task_time = utc_ctime + time_delay
        # result = send_sms.apply_async(["911", ], eta=task_time)
        # print(result.id)

        # img = self.get_object()  # 获取详情的实例对象
        # mcs = img.mcs
        # if mcs.file_upload_id == 0:  # The file is not synchronized to the MCS
        #     mcs.file_upload_id, mcs.nft_url = upload_file_pay(wallet_info, img.src.path)
        #     mcs.save()
        #
        #     msg = 'The file is not synchronized to the MCS'
        # else:
        #     msg = 'The file already synchronized to the MCS, the file_upload_id is %d' % mcs.file_upload_id


        # print(img.src.path)
        # if not hasattr(img, 'mcs'):  # 判断是否又对应的mcs存储
        #
        #     source_file_upload_id, nft_uri = upload_file_pay(wallet_info, img.src.path)
        #     data = {
        #         "img": img.id,
        #         "file_upload_id": source_file_upload_id,
        #         "nft_url": nft_uri,
        #     }
        #     # 调用序列化器进行反序列化验证和转换
        #     serializer = McsSerializer(data=data)
        #     # 当验证失败时,可以直接通过声明 raise_exception=True 让django直接跑出异常,那么验证出错之后，直接就再这里报错，程序中断了就
        #
        #     result = serializer.is_valid(raise_exception=True)
        #     print("验证结果:%s" % result)
        #
        #     print(serializer.errors)  # 查看错误信息
        #
        #     # 获取通过验证后的数据
        #     print(serializer.validated_data)  # form -- clean_data
        #     # 保存数据
        #     mcs_obj = serializer.save()
        #     # mcs_obj = Mcs.objects.create(
        #     #     img=serializer.validated_data.get("img"),
        #     #     file_upload_id=serializer.validated_data.get("file_upload_id"),
        #     #     nft_url=serializer.validated_data.get("nft_url")
        #     # )
        #     msg = 'success to make a copy into mac'
        # else:
        #     msg = 'there is already have mac info related to this img: file id is %d' % img.mcs.file_upload_id

        # print(msg)

        # return Response({"data": msg, 'code': 200})
        return Response({"data": 'msg', 'code': 200})


class McsViewSet(viewsets.ModelViewSet):
    queryset = Mcs.objects.all().order_by('-id')
    serializer_class = McsSerializer
    # permission_classes = (AllowAny,)
    pagination_class = GalleryPageNumberPagination  # could disp the filter button in the web
