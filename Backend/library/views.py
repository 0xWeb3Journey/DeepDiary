from datetime import datetime, timedelta

from celery.result import AsyncResult
from django.db.models import Count, Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from rest_framework.decorators import action
from rest_framework.response import Response
from taggit.models import Tag

from deep_diary.config import wallet_info
from face.models import FaceAlbum
from face.task import get_all_fts
from library.filters import ImgFilter, ImgSearchFilter, CategoryFilter
from library.models import Img, Category, Mcs, Address
from library.pagination import GalleryPageNumberPagination
from library.serializers import ImgSerializer, ImgDetailSerializer, ImgCategorySerializer, McsSerializer, \
    CategorySerializer
from library.task import save_img_info, upload_img_to_mcs, upload_to_mcs, set_img_tags, set_all_img_tags, \
    set_img_colors, set_img_categories, set_all_img_categories, save_all_img_info, set_all_img_group, \
    add_all_img_colors_to_category, set_all_img_address
from library.task import send_email

from mycelery.library.tasks import send_sms
from mycelery.main import app
from utils.mcs_storage import upload_file_pay, approve_usdc

#
# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     pagination_class = GalleryPageNumberPagination  # could disp the filter button in the web
#     # 第一种方法
#     filter_class = CategoryFilter  # 过滤类
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter,
#                        filters.OrderingFilter]  # 模糊过滤，注意的是，这里的url参数名变成了?search=搜索内容
from utils.pagination import GeneralPageNumberPagination


class ImgCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = ImgCategorySerializer


class ImgViewSet(viewsets.ModelViewSet):
    queryset = Img.objects.all().order_by('-id')

    serializer_class = ImgSerializer
    # permission_classes = (AllowAny,)
    pagination_class = GalleryPageNumberPagination  # could disp the filter button in the web
    # 第一种方法
    filter_class = ImgFilter  # 过滤类

    # search_class = ImgSearchFilter
    # 第二种方法
    # DjangoFilterBackend  # 精准过滤，字段用filterset_fields定义
    # filters.SearchFilter  # 模糊搜索，字段用search_fields
    # filters.OrderingFilter  # 排序规则字段定义
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]  # 模糊过滤，注意的是，这里的url参数名变成了?search=搜索内容

    # The SearchFilter class will only be applied if the view has a search_fields attribute set.
    # The search_fields attribute should be a list of names of text type fields on the model,
    # such as CharField or TextField.
    # The search parameter may contain multiple search terms, which should be whitespace and/or comma separated
    # search_fields = ['user__username', 'address__location', 'tags__name', 'dates__year', 'dates__month', 'dates__day']
    # search_fields = ['$tags__name']  # 如何使用正则进行匹配

    search_fields = {
        # color
        'colors__image__closest_palette_color_parent': ['exact'],

        # category
        'categories__name': ['exact'],  #
        'categories__type': ['exact'],  #
        'categories__value': ['exact'],  #
        # address
        'address__country': ['exact', 'contains'],
        'address__province': ['exact', 'contains'],
        'address__city': ['exact', 'contains'],
        'address__district': ['exact', 'contains'],
        'address__location': ['icontains'],
        # face
        'faces__name': ['exact', 'icontains'],  #
        # date
        'dates__year': ['exact', 'contains'],  #
        'dates__month': ['exact', 'contains'],  #
        'dates__day': ['exact', 'contains'],  #
        'dates__capture_date': ['exact', 'contains'],  #

        '$tags__name': ['exact', 'icontains'],  #
        # img
        'name': ['exact', 'icontains'],  #
        'title': ['exact', 'icontains'],  #
        'caption': ['exact', 'icontains'],  #
        "type": ['exact'],
    }

    ordering_fields = ['id', 'dates__capture_date']  # 这里的字段，需要总上面定义字段中选择

    def perform_create(self, serializer):
        print(f"INFO:{self.request.user}")
        instance = serializer.save(user=self.request.user)
        print(f'INFO: Img start perform_create........{instance.src}')
        # save_img_info.delay(instance)  # if this add the delay function, this function will be processed by celery
        # set_img_tags.delay(instance)  # if this add the delay function, this function will be processed by celery
        # set_img_colors(instance)  # if this add the delay function, this function will be processed by celery
        # set_img_categories(instance)  # if this add the delay function, this function will be processed by celery

        # upload_img_to_mcs.delay(instance)
        # upload_img_to_mcs(instance)  # Cannot run in parallel

        # w3_api = approve_usdc(wallet_info)

    def perform_update(self, serializer):  # 应该在调用的模型中添加
        # print(f'图片更新：{self.request.data}')
        instance = serializer.save()  # ProcessedImageField, 也就是ImageField的实例对象
        print(f'INFO: start perform_update........data is: {serializer.validated_data}')

        # print(f"INFO: instance.src: {instance.src}")
        # print(f"INFO: instance.src.name: {instance.src.name}")
        # print(f"INFO: instance.src__name: {os.path.basename(instance.src.name)}")
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

    # def get_queryset(self):
    #     # faces_num couldn't filter in the django-filter since this is based on the annotate
    #     faces_num = self.request.query_params.get('faces_num')
    #     if faces_num:
    #         return self.queryset \
    #             .annotate(faces_num=Count('faces')).filter(faces_num=faces_num)  # annotate the faces_num here
    #
    #     return self.queryset

    @action(detail=True, methods=['get'])  # 在详情中才能使用这个自定义动作
    def set_colors(self, request, pk=None):  # 当detail=True 的时候，需要指定第三个参数，如果未指定look_up, 默认值为pk，如果指定，该值为loop_up的值
        img = self.get_object()  # 获取详情的实例对象
        print(f'INFO pk: {pk}')
        print(f'INFO img: {type(img)}')
        print(f'INFO img: {img.id}')
        # print(f'INFO request: {dir(request)}')

        set_img_colors(img)

        serializer = ImgDetailSerializer(img, many=False, context={'request': request})  # 不报错
        # serializer = ImgSerializer(img, many=False)  # 报错
        # serializer = self.get_serializer(img)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])  # 在详情中才能使用这个自定义动作
    def test(self, request, pk=None):  # 当detail=True 的时候，需要指定第三个参数，如果未指定look_up, 默认值为pk，如果指定，该值为loop_up的值
        # img = self.get_object()  # 获取详情的实例对象
        # print(f'INFO pk: {pk}')
        # print(f'INFO img: {type(img)}')
        # print(f'INFO img: {img.id}')
        # print(f'INFO request: {dir(request)}')

        # save_img_info(img)
        # set_img_colors(img)
        # set_img_categories(img)
        # set_all_img_categories()
        # save_all_img_info()
        # set_all_img_address()
        # add_all_img_colors_to_category()

        # serializer = ImgDetailSerializer(img, many=False, context={'request': request})  # 不报错
        # serializer = ImgSerializer(img, many=False)  # 报错
        # serializer = self.get_serializer(img)
        # return Response(serializer.data)

        # filter_class = self.filter_class
        # print(filter_class)
        data = {
            'categories': {
                'person': '人物',
                'organization': '机构',
                'location': '地点',
            },
            "data": {
                "nodes": [
                    {"id": "1", "label": "bluejoe", "image": "https://bluejoe2008.github.io/bluejoe3.png",
                     "categories": ["person"]},
                    {"id": "2", "label": "CNIC", "image": "https://bluejoe2008.github.io/cas.jpg",
                     "categories": ["organization"]},
                    {"id": "3", "label": "beijing", "image": "https://bluejoe2008.github.io/beijing.jpg",
                     "categories": ["location"]}
                ],
                "edges": [
                    {"from": "1", "to": "2", "label": "work for"},
                    {"from": "1", "to": "3", "label": "live in"},
                    {"from": "2", "to": "3", "label": "test"}
                ]
            }
        }
        return Response(data)
        # return Response({"msg": "success"})

    @action(detail=False, methods=['get'])  # 在详情中才能使用这个自定义动作
    def check_mcs(self, request, pk=None):
        print('---------------------------------------checking mcs')
        upload_to_mcs.delay()
        data = {
            "data": '',
            'code': 200,
            'msg': 'All the images have been uploaded successfully, will start synchronize to MCS now'
        }
        return Response(data)

    @action(detail=False, methods=['get'])  # 在详情中才能使用这个自定义动作
    def set_tags(self, request, pk=None):
        print('---------------------------------------setting tags')
        # img_obj = self.get_object()  # 获取详情的实例对象
        # set_img_tags(img_obj)
        set_all_img_tags.delay()
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

        # return Response({"data": msg, 'code': 200})

        data = {
            "data": '',
            'code': 200,
            'msg': 'success to get the tags'
        }
        return Response(data)


class McsViewSet(viewsets.ModelViewSet):
    queryset = Mcs.objects.all().order_by('-id')
    serializer_class = McsSerializer
    # permission_classes = (AllowAny,)
    pagination_class = GalleryPageNumberPagination  # could disp the filter button in the web


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    # permission_classes = (AllowAny,)
    pagination_class = GeneralPageNumberPagination  # could disp the filter button in the web
    # 第一种方法
    filter_class = CategoryFilter  # 过滤类
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]  # 模糊过滤，注意的是，这里的url参数名变成了?search=搜索内容

    @action(detail=False, methods=['get'])  # 在详情中才能使用这个自定义动作
    def get_filter_list(self, request, pk=None):  # 当detail=True 的时候，需要指定第三个参数，如果未指定look_up, 默认值为pk，如果指定，该值为loop_up的值
        data = {
            'fc_nums': Img.objects.annotate(fc_nums=Count('faces')).values_list('fc_nums',
                                                                                flat=True).distinct().order_by(
                'fc_nums'),
            'fc_name': FaceAlbum.objects.annotate(value=Count('img')).filter(value__gte=1).values('name',
                                                                                                  'value').distinct().order_by(
                '-value'),

            # 'tags': Img.objects.values_list('tags__name', flat=True).distinct().order_by('tags__name'),
            'tags': Tag.objects.annotate(value=Count('imgs')).filter(value__gt=0).order_by('-value').values('name',
                                                                                                            'value'),

            # 'c_img': Img.objects.filter(categories__type='img_color').values('categories__name', 'categories__value').distinct().order_by('categories__name'),
            'c_img': Category.objects.filter(type='img_color').values('name', 'value').distinct().order_by('name'),
            'c_back': Category.objects.filter(type='back_color').values('name', 'value').distinct().order_by('name'),
            'c_fore': Category.objects.filter(type='fore_color').values('name', 'value').distinct().order_by('name'),
            'category': Category.objects.filter(type='category').annotate(img_nums=Count('img')).values('name',
                                                                                                        'img_nums').distinct().order_by(
                '-img_nums'),
            'group': Category.objects.filter(type='group').annotate(img_nums=Count('img')).values('name',
                                                                                                  'img_nums').distinct().order_by(
                '-img_nums'),
            'city': Category.objects.filter(type='address').annotate(img_nums=Count('img')).values('name',
                                                                                                   'img_nums').distinct().order_by(
                '-img_nums'),

            'layout': ['Square', 'Wide', 'Tall'],
            'size': ['Small', 'Medium', 'Large', 'Extra large', 'At least'],
            'license': ['Public domain', 'Free to share and use', 'Free to share and use commercially'],
            'ordering': ['id', '-id', 'dates__capture_date', '-dates__capture_date']

        }
        # data['tags'] = list(data['tags'])
        # data['tags'].insert(0, 'All')
        # # 循环判断是否有all字段，如果没有，则转换成列表并插入
        return Response({
            'msg': 'success',
            'code': 200,
            'data': data,
        })
