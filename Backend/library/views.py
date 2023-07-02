from io import BytesIO

import cv2
import numpy as np
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from taggit.models import Tag

from library.filters import ImgFilter, CategoryFilter, AddressFilter
from library.models import Img, Category, Address, Stat, Evaluate, Date, ImgMcs, Face
from library.pagination import GalleryPageNumberPagination, AddressNumberPagination, FacePageNumberPagination
from library.serializers import ImgSerializer, ImgDetailSerializer, ImgCategorySerializer, McsSerializer, \
    CategorySerializer, AddressSerializer, CategoryDetailSerializer, FaceSerializer, FaceBriefSerializer
from library.serializers_out import CategoryBriefSerializer
from library.task import ImgProces
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
        print(f"INFO:Img start perform_create, {self.request.user}")
        print(f"INFO:Img file, {self.request.FILES}")
        file = self.request.FILES.get("src")
        f_path = file.temporary_file_path()
        print(f"INFO:temporary_file_path, {f_path}")

        instance = serializer.save(user=self.request.user)

        # get_list = ['get_exif_info', 'get_tags', 'get_colors', 'get_categories',
        #             'get_faces']  # get_exif_info 必须第一个，因为是这个函数创建了stat实例
        # # get_list = ['get_exif_info', 'get_faces']
        # add_list = ['add_date_to_category', 'add_location_to_category', 'add_group_to_category',
        #             'add_colors_to_category']
        # # add_list = ['add_colors_to_category']
        #
        # img_process = ImgProces(instance=instance)
        # img_process.get_img(img_process, instance=instance, func_list=get_list, force=True)
        #
        # img_process.add_img_to_category(img_process, instance=instance, func_list=add_list)

    def perform_update(self, serializer):  # 应该在调用的模型中添加
        data = self.request.data
        print(f'图片更新：{data}')
        instance = self.get_object()  # 获取详情的实例对象
        serializer.save()  # 保存更新的实例对象

        if 'tags' in data:
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
    @action(detail=False, methods=['get'])  # 在详情中才能使用这个自定义动作
    def init(self, request, pk=None):
        print('------------------init the system------------------')
        img_process = ImgProces()
        img_process.category_init()
        return Response({"msg": "init success"})

    @action(detail=False, methods=['get'])  # 在详情中才能使用这个自定义动作
    def batch_img_process(self, request, pk=None):
        print('------------------batch_img_test------------------')

        get_list = ['get_exif_info', 'get_tags', 'get_colors', 'get_categories',
                    'get_faces']  # get_exif_info 必须第一个，因为是这个函数创建了stat实例
        # get_list = ['get_exif_info', 'get_faces']
        add_list = ['add_date_to_category', 'add_location_to_category', 'add_group_to_category',
                    'add_colors_to_category']
        # add_list = ['add_colors_to_category']

        img_process = ImgProces()
        img_process.get_all_img(img_process, func_list=get_list, force=True)

        img_process.add_all_img_to_category(img_process,  func_list=add_list)
        return Response({"msg": "batch_img_test success"})

    @action(detail=True, methods=['get'])  # 在详情中才能使用这个自定义动作
    def img_process(self, request, pk=None):  # 当detail=True 的时候，需要指定第三个参数，如果未指定look_up, 默认值为pk，如果指定，该值为loop_up的值
        print('------------------img_test------------------')
        instance = self.get_object()  # 获取详情的实例对象

        get_list = ['get_exif_info', 'get_tags', 'get_colors', 'get_categories',
                    'get_faces']  # get_exif_info 必须第一个，因为是这个函数创建了stat实例
        # get_list = ['get_exif_info', 'get_faces']
        add_list = ['add_date_to_category', 'add_location_to_category', 'add_group_to_category',
                    'add_colors_to_category']
        # add_list = ['add_colors_to_category']

        img_process = ImgProces(instance=instance)
        img_process.get_img(img_process, instance=instance, func_list=get_list, force=True)

        img_process.add_img_to_category(img_process, instance=instance, func_list=add_list)

        print('------------------img_test finished------------------')
        return Response({"msg": 'img_test finished'})

    @action(detail=False, methods=['get'])  # will be used in the list view since the detail = false
    def upload_finished(self, request, pk=None):
        # TODO do something after uploading the image
        data = {
            "data": '',
            'code': 200,
            'msg': 'All the images have been uploaded successfully'
        }
        return Response(data)


class ImgMcsViewSet(viewsets.ModelViewSet):
    queryset = ImgMcs.objects.all().order_by('-id')
    serializer_class = McsSerializer
    # permission_classes = (AllowAny,)
    pagination_class = GalleryPageNumberPagination  # could disp the filter button in the web


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().annotate(img_nums=Count('imgs')).order_by('-img_nums')  # ordered by the
    # queryset = Category.objects.filter(is_root=True).annotate(img_nums=Count('imgs')).order_by('-img_nums')
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
            # 'fc_name': FaceAlbum.objects.annotate(value=Count('imgs')).filter(value__gte=1).values('name',
            #                                                                                       'value').distinct().order_by(
            #     '-value'),

            # 'tags': Img.objects.values_list('tags__name', flat=True).distinct().order_by('tags__name'),
            'tags': Tag.objects.annotate(value=Count('imgs')).filter(value__gt=0).order_by('-value').values('name',
                                                                                                            'value'),

            # 'c_img': Category.objects.filter(type='img_color').values('name', 'value').distinct().order_by('name'),
            # 'c_back': Category.objects.filter(type='back_color').values('name', 'value').distinct().order_by('name'),
            # 'c_fore': Category.objects.filter(type='fore_color').values('name', 'value').distinct().order_by('name'),
            # 'category': Category.objects.filter(type='category').annotate(img_nums=Count('imgs')).values('name',
            #                                                                                              'img_nums').distinct().order_by(
            #     '-img_nums'),
            # 'group': Category.objects.filter(type='group').annotate(img_nums=Count('imgs')).values('name',
            #                                                                                        'img_nums').distinct().order_by(
            #     '-img_nums'),
            # 'city': Category.objects.filter(type='address').annotate(img_nums=Count('imgs')).values('name',
            #                                                                                         'img_nums').distinct().order_by(
            #     '-img_nums'),

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

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryBriefSerializer
        else:
            return CategorySerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all().order_by('img')
    serializer_class = AddressSerializer
    # permission_classes = (AllowAny,)
    pagination_class = AddressNumberPagination  # could disp the filter button in the web

    filter_class = AddressFilter  # 过滤类
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]  # 模糊过滤，注意的是，这里的url参数名变成了?search=搜索内容


class FaceViewSet(viewsets.ModelViewSet):
    queryset = Face.objects.all()
    pagination_class = FacePageNumberPagination  # 增加了这句代码，就无法显示filter,不过效果还是有的

    # serializer_class = FaceBriefSerializer
    # permission_classes = (AllowAny,)
    # pagination_class = FacePageNumberPagination  # 增加了这句代码，就无法显示filter,不过效果还是有的
    #
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter,
    #                    filters.OrderingFilter]  # 模糊过滤，注意的是，这里的url参数名变成了?search=搜索内容
    # filterset_fields = ['profile__id', 'img__id']  # 外键需要增加2个下划线
    # # filterset_fields = ['img', 'name', 'is_confirmed', 'face_score']
    # search_fields = ['profile__id', 'img__id']
    # ordering_fields = ['img__id']  # 这里的字段，需要总上面定义字段中选择

    # def perform_create(self, serializer):
    # print(f"INFO:{self.request.user}")
    # serializer.save(user=self.request.user)
    #     pass
    #
    def perform_update(self, serializer):  # 应该在调用的模型中添加
        print(f'人脸更新：validated_data =  {serializer.validated_data}')
        print(f'人脸更新：validated_data =  {self.request.data.get("name", None)}')
        print(f'当前访问人脸的用户是 =  {self.request.user}')

        fc = self.get_object()
        process = ImgProces()
        faces = process.face_rename(fc, self.request.data.get('name', None))
        # change_face_name.delay(fc, serializer)  # 如果执行了改名，则返回真，人脸改名后，确认状态自动为True
        # if not change_face_name(fc, serializer):  # 如果执行了改名，则返回真，人脸改名后，确认状态自动为True
        #     change_confirm_state(fc, serializer)  # 人名已经是识别出来的名字，进行确认后，同样要计算人脸特征

    def get_serializer_class(self):
        if self.action == 'list':
            print(self.action)
            return FaceBriefSerializer
        else:
            return FaceSerializer
