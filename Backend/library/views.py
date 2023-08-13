import json
from io import BytesIO

import cv2
import numpy as np
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from taggit.models import Tag

from deep_diary.settings import calib
from library.filters import ImgFilter, CategoryFilter, AddressFilter, FaceFilter
from library.models import Img, Category, Address, Stat, Evaluate, Date, ImgMcs, Face
from library.pagination import GalleryPageNumberPagination, AddressNumberPagination, FacePageNumberPagination
from library.serializers import ImgSerializer, ImgDetailSerializer, ImgCategorySerializer, McsSerializer, \
    CategorySerializer, AddressSerializer, CategoryDetailSerializer, FaceSerializer, FaceBriefSerializer
from library.serializers_out import CategoryBriefSerializer, ImgGraphSerializer
from library.task import ImgProces
from user_info.models import Profile
from user_info.serializers_out import ProfileGraphSerializer, ProfileBriefSerializer
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

    search_fields = filter_class.search_fields

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

    def get_queryset(self):
        # Perform additional data processing on the request
        param = self.request.query_params

        # print(f'INFO:-> param: {param}')

        if param:
            # Do something with the param, for example, filter the queryset based on the param
            # self.queryset = self.queryset.filter(some_field=param.get('some_field', None))
            pass

        # Get the filtered queryset using the parent class method
        queryset = super().get_queryset()

        return queryset

    def img_pre_process(self):
        # 从request中获取参数
        param = self.request.query_params
        print(f'INFO:-> param: {param}')

        force = param.get("force", None)
        get_list_org = param.get("get_list", None)
        add_list_org = param.get("add_list", None)

        # get_exif_info 必须第一个，因为是这个函数创建了stat实例
        # param得到的都是字符类型，需要转换成bool类型
        force = True if force == '1' else False  # force = 1, True, force = 0, False
        get_list = [item.strip() for item in get_list_org.split(',') if item != '']  # 去掉空字符串
        add_list = [item.strip() for item in add_list_org.split(',') if item != '']

        if get_list_org == 'all':
            print('INFO:-> get_list_org == all')
            get_list = ['get_exif_info', 'get_tags', 'get_colors', 'get_categories',
                        'get_faces']
        if add_list_org == 'all':
            print('INFO:-> add_list_org == all')
            add_list = ['add_date_to_category', 'add_location_to_category', 'add_group_to_category',
                        'add_colors_to_category']
        print(f'INFO:-> param force: {force}')
        print(f'INFO:-> param get_list: {get_list_org}')
        print(f'INFO:-> param add_list: {add_list_org}')
        return force, get_list, add_list

    @action(detail=False, methods=['get'])  # 在详情中才能使用这个自定义动作
    def init(self, request, pk=None):
        print('------------------init the system------------------')
        img_process = ImgProces()
        img_process.category_init()
        return Response({"msg": "init success"})

    @action(detail=False, methods=['get'])  # 在详情中才能使用这个自定义动作
    def batch_img_process(self, request, pk=None):
        print('------------------batch_img_test------------------')
        force, get_list, add_list = self.img_pre_process()

        img_process = ImgProces()
        img_process.get_all_img(img_process, func_list=get_list, force=force)

        img_process.add_all_img_to_category(img_process, func_list=add_list)
        return Response({"msg": "batch_img_test success"})

    @action(detail=True, methods=['get'])  # 在详情中才能使用这个自定义动作
    def img_process(self, request, pk=None):  # 当detail=True 的时候，需要指定第三个参数，如果未指定look_up, 默认值为pk，如果指定，该值为loop_up的值
        print('------------------img_process------------------')
        instance = self.get_object()  # 获取详情的实例对象
        force, get_list, add_list = self.img_pre_process()

        img_process = ImgProces(instance=instance)
        if get_list:
            print(f'INFO:-> param get_list: {get_list}')
            img_process.get_img(img_process, instance=instance, func_list=get_list, force=force)
        if add_list:
            print(f'INFO:-> param add_list: {add_list}')
            img_process.add_img_to_category(img_process, instance=instance, func_list=add_list)

        print('------------------img_process finished------------------')
        return Response({"msg": 'img_process finished'})

    @action(detail=False, methods=['get'])  # will be used in the list view since the detail = false
    def upload_finished(self, request, pk=None):
        print('------------------upload_finished------------------')
        print(self.request.query_params)
        queryset = self.get_queryset()
        print(len(queryset))
        filteref_queryset = self.filter_queryset(queryset)
        print(len(filteref_queryset))
        # TODO do something after uploading the image
        data = {
            "data": '',
            'code': 200,
            'msg': 'All the images have been uploaded successfully'
        }
        return Response(data)

    @action(detail=False, methods=['get'])  # 在详情中才能使用这个自定义动作
    def graph(self, request, pk=None):  # 当detail=True 的时候，需要指定第三个参数，如果未指定look_up, 默认值为pk，如果指定，该值为loop_up的值
        # objs = FaceAlbum.objects.annotate(value=Count('faces')).order_by('-value')
        # serializer = FaceAlbumGraphSerializer(self.queryset.exclude(name__startswith='unknown'), many=True, context={'request': request})  # 不报错
        # person_node = serializer.data
        img_serializer = ImgGraphSerializer(self.queryset, many=True, context={'request': request})
        img_node = img_serializer.data
        person_searilaizer = ProfileGraphSerializer(Profile.objects.all(), many=True, context={'request': request})  # 这里需要传入查询集
        persion_node = person_searilaizer.data
        edges = self.get_relation_of_img_profile()
        # print(json.dumps(edges, indent=4, ensure_ascii=False))

        graph = {
            "categories": {
                "date": "时间",
                "location": "地点",
                "person": "人物",
                "event": "事件",
                "image": "图片",
                "video": "视频",
                "voice": "语音",
                "company": "公司",
            },
            "data": {
                "nodes": img_node + persion_node,
                "edges": edges
            }
        }

        # demo
        # data = {
        #     "categories": {
        #         "date": "时间",
        #         "location": "地点",
        #         "person": "人物",
        #         "event": "事件",
        #         "image": "图片",
        #         "video": "视频",
        #         "voice": "语音",
        #         "company": "公司",
        #     },
        #     "data": {
        #         "nodes": [
        #             {
        #                 "id": 1,
        #                 "label": "deep-diary",
        #                 "image": "http://127.0.0.1:8000/media/CACHE/images/blue/img/1970/01/01/b1fc6cc28c297f6910f267da332d7fc8/7bb5bfc1d897419122805b02b8a0379e.jpeg",
        #                 "value": 30,
        #                 "desc": "make your own data values",
        #                 "categories": [
        #                     "company"
        #                 ]
        #             },
        #             {
        #                 "id": 2,
        #                 "label": "blue",
        #                 "image": "http://127.0.0.1:8000/media/face/face_aQVml.jpg",
        #                 "value": 30,
        #                 "desc": "deep-diary creator",
        #                 "categories": [
        #                     "person"
        #                 ]
        #             },
        #             {
        #                 "id": 3,
        #                 "label": "prepare for the live broadcast",
        #                 "image": "http://127.0.0.1:8000/media/CACHE/images/blue/img/1970/01/01/1310f1459e8cabf0e02cea3fd5960e7d/c8212dc44d7c29de7843e74580f5cb8b.jpeg",
        #                 "value": 40,
        #                 "desc": "won the 6th in the Hackathon competition, after that, our team need to have a live "
        #                         "stream on Oct. 21th to present our project, that is important to us, so we prepare "
        #                         "for it every day",
        #                 "categories": [
        #                     "event"
        #                 ]
        #             },
        #             {
        #                 "id": 4,
        #                 "label": "2022-10",
        #                 "image": "http://127.0.0.1:8000/media/CACHE/images/blue/img/1970/01/01/avatar_TqNd2Yf/b9f276c6f29f62239a4d23e8d0dc0bd5.jpg",
        #                 "value": 30,
        #                 "desc": "this event happened on this month",
        #                 "categories": [
        #                     "date"
        #                 ]
        #             },
        #             {
        #                 "id": 5,
        #                 "label": "Ningbo",
        #                 "image": "http://127.0.0.1:8000/media/CACHE/images/blue/img/1970/01/01/5d14677a3fa465509513930caeacf2b2/018d88d7b9718578a44fa66738c3496c.jpeg",
        #                 "value": 30,
        #                 "desc": "location of this event",
        #                 "categories": [
        #                     "location"
        #                 ]
        #             },
        #             {
        #                 "id": 6,
        #                 "label": "img1",
        #                 "image": "http://127.0.0.1:8000/media/CACHE/images/blue/img/1970/01/01/e8e4be52ba59a1a124665c82bb3f5ae2/02ef4bc0bd7a2f7c593296a416974cfc.jpeg",
        #                 "value": 30,
        #                 "desc": "image memories of this event",
        #                 "categories": [
        #                     "image"
        #                 ]
        #             },
        #             {
        #                 "id": 7,
        #                 "label": "img2",
        #                 "image": "http://127.0.0.1:8000/media/CACHE/images/blue/img/1970/01/01/aaf757201bbf5a549ceab52008817eb7/94eb614e5cd71d70e9ceab22c3c4583f.jpeg",
        #                 "value": 30,
        #                 "desc": "image memories of this event",
        #                 "categories": [
        #                     "image"
        #                 ]
        #             },
        #             {
        #                 "id": 8,
        #                 "label": "video1",
        #                 "image": "http://127.0.0.1:8000/media/CACHE/images/blue/img/1970/01/01/14521c818922da50f83c2bfa7189db0b/df4b5d9b47f2c8cf2d69590316f58c88.jpeg",
        #                 "value": 30,
        #                 "desc": "video memories of this event",
        #                 "categories": [
        #                     "video"
        #                 ]
        #             },
        #             {
        #                 "id": 9,
        #                 "label": "voice1",
        #                 "image": "http://127.0.0.1:8000/media/CACHE/images/blue/img/1970/01/01/69a8364435cf80991f383a575afa77e5/dae181e5d1e22c0e2e91ccc6084270cb.jpeg",
        #                 "value": 30,
        #                 "desc": "voice memories of this event",
        #                 "categories": [
        #                     "voice"
        #                 ]
        #             },
        #
        #             {
        #                 "id": 10,
        #                 "label": "Design the databased structure of deep-diary",
        #                 "image": "http://127.0.0.1:8000/media/CACHE/images/blue/img/1970/01/01/1f823568d8eafa515b055fc9d0b0caf3/2b59b6af416b24dd3adad28319f67923.jpeg",
        #                 "value": 40,
        #                 "desc": "graph display is attractive for human, but the relationship between is complex, "
        #                         "so we need take some time to find out all the realtionships between each nodes",
        #                 "categories": [
        #                     "event"
        #                 ]
        #             },
        #             {
        #                 "id": 12,
        #                 "label": "2022-11",
        #                 "image": "http://127.0.0.1:8000/media/CACHE/images/blue/img/1970/01/01/301112218b977280ffd5ce64eda157e2/2b5a057ee68c5f158749ad5eb408d800.jpeg",
        #                 "value": 30,
        #                 "desc": "this event happened on this month",
        #                 "categories": [
        #                     "date"
        #                 ]
        #             },
        #             {
        #                 "id": 11,
        #                 "label": "Taizhou",
        #                 "image": "http://127.0.0.1:8000/media/CACHE/images/blue/img/1970/01/01/bdf36d3cca08de7c0331e08d84c9d18b/b0b08588af28e8f0c4549329c7e27387.jpeg",
        #                 "value": 30,
        #                 "desc": "location of this event",
        #                 "categories": [
        #                     "location"
        #                 ]
        #             },
        #             {
        #                 "id": 13,
        #                 "label": "video2",
        #                 "image": "http://127.0.0.1:8000/media/CACHE/images/blue/img/1970/01/01/0b40b4ae6f872c2358abdc8401fcd8bb/7955fb802fd8d9237be98cc60e2d50fe.jpeg",
        #                 "value": 30,
        #                 "desc": "video memories of this event",
        #                 "categories": [
        #                     "video"
        #                 ]
        #             },
        #             {
        #                 "id": 14,
        #                 "label": "voice2",
        #                 "image": "http://127.0.0.1:8000/media/CACHE/images/blue/img/1970/01/01/b4dccead83555244d5d065aa12965006/4fc85f59caf86359360b2d10611bca8d.jpg",
        #                 "value": 30,
        #                 "desc": "voice memories of this event",
        #                 "categories": [
        #                     "voice"
        #                 ]
        #             },
        #
        #         ],
        #         "edges": [
        #             {
        #                 "from": 2,
        #                 "to": 1,
        #                 "label": "work in"
        #             },
        #             {
        #                 "from": 2,
        #                 "to": 3,
        #                 "label": "join in"
        #             },
        #             # 伪代码如下
        #             {
        #                 "from": img.id,
        #                 "to": img.profiles.id,
        #                 "label": "include"
        #             }
        #         ]
        #             # {
        #             #     "from": 2,
        #             #     "to": 5,
        #             #     "label": "live in"
        #             # },
        #             # {
        #             #     "from": 2,
        #             #     "to": 11,
        #             #     "label": "hometown"
        #             # },
        #             {
        #                 "from": 3,
        #                 "to": 4,
        #                 "label": "happened on"
        #             },
        #             {
        #                 "from": 3,
        #                 "to": 5,
        #                 "label": "located in"
        #             },
        #             {
        #                 "from": 3,
        #                 "to": 6,
        #                 "label": "recorded by"
        #             },
        #             {
        #                 "from": 3,
        #                 "to": 7,
        #                 "label": "recorded by"
        #             },
        #             {
        #                 "from": 3,
        #                 "to": 8,
        #                 "label": "recorded by"
        #             },
        #             {
        #                 "from": 3,
        #                 "to": 9,
        #                 "label": "recorded by"
        #             },
        #
        #             {
        #                 "from": 10,
        #                 "to": 11,
        #                 "label": "happened on"
        #             },
        #             {
        #                 "from": 10,
        #                 "to": 12,
        #                 "label": "located in"
        #             },
        #             {
        #                 "from": 10,
        #                 "to": 13,
        #                 "label": "recorded by"
        #             },
        #             {
        #                 "from": 10,
        #                 "to": 14,
        #                 "label": "recorded by"
        #             },
        #
        #         ]
        #     }
        # }

        # database demo
        # data = {
        #     "categories": {
        #         "date": "时间",
        #         "location": "地点",
        #         "person": "人物",
        #         "event": "事件",
        #         "image": "图片",
        #         "video": "视频",
        #         "voice": "语音",
        #         "company": "公司",
        #         "info": "信息",
        #     },
        #     "data": {
        #         "nodes": [
        #             {
        #                 "id": 1,
        #                 "label": "User",
        #                 "value": 20,
        #                 "desc": "Django build-in User model.",
        #                 "categories": [
        #                     "info"
        #                 ]
        #             },
        #             {
        #                 "id": 2,
        #                 "label": "Profile",
        #                 "value": 30,
        #                 "image": "http://127.0.0.1:8000/media/face/face_aQVml.jpg",
        #                 "desc": "inherit build-in AbstractUser model.",
        #                 "categories": [
        #                     "person"
        #                 ]
        #             },
        #             {
        #                 "id": 3,
        #                 "label": "Company",
        #                 "value": 20,
        #                 "desc": "one to one relationship to Experience model.",
        #                 "categories": [
        #                     "company"
        #                 ]
        #             },
        #             {
        #                 "id": 4,
        #                 "label": "Experience",
        #                 "value": 20,
        #                 "desc": "working experience of this user.",
        #                 "categories": [
        #                     "info"
        #                 ]
        #             },
        #             {
        #                 "id": 5,
        #                 "label": "Supply",
        #                 "value": 20,
        #                 "desc": "the resources that the user could provide",
        #                 "categories": [
        #                     "info"
        #                 ]
        #             },
        #             {
        #                 "id": 6,
        #                 "label": "Demand",
        #                 "value": 20,
        #                 "desc": "the resources that the user that needed",
        #                 "categories": [
        #                     "info"
        #                 ]
        #             },
        #             {
        #                 "id": 7,
        #                 "label": "Event",
        #                 "value": 20,
        #                 "desc": "could understand like diary which not based on the date, but based on the event",
        #                 "categories": [
        #                     "event"
        #                 ]
        #             },
        #             {
        #                 "id": 8,
        #                 "label": "Category",
        #                 "value": 20,
        #                 "desc": "auto category all the images based on the deep learning",
        #                 "categories": [
        #                     "info"
        #                 ]
        #             },
        #             {
        #                 "id": 9,
        #                 "label": "Img",
        #                 "value": 30,
        #                 "image": "http://127.0.0.1:8000/media/blue/img/1970/01/01/b1fc6cc28c297f6910f267da332d7fc8.jpeg",
        #                 "desc": "img is the most important memory element",
        #                 "categories": [
        #                     "image"
        #                 ]
        #             },
        #             {
        #                 "id": 10,
        #                 "label": "ImgCategory",
        #                 "value": 20,
        #                 "desc": "intermediate table of Img and Category",
        #                 "categories": [
        #                     "info"
        #                 ]
        #             },
        #             {
        #                 "id": 11,
        #                 "label": "FaceAlbum",
        #                 "value": 20,
        #                 "desc": "Person face interface",
        #                 "categories": [
        #                     "info"
        #                 ]
        #             },
        #             {
        #                 "id": 12,
        #                 "label": "Face",
        #                 "value": 30,
        #                 "image": "http://127.0.0.1:8000/media/face/face_42tyr.jpg",
        #                 "desc": "intermediate table of Img and FaceAlbum",
        #                 "categories": [
        #                     "info"
        #                 ]
        #             },
        #             {
        #                 "id": 13,
        #                 "label": "Video",
        #                 "value": 20,
        #                 "desc": "daily video",
        #                 "categories": [
        #                     "video"
        #                 ]
        #             },
        #             {
        #                 "id": 14,
        #                 "label": "Voice",
        #                 "value": 20,
        #                 "desc": "daily voice",
        #                 "categories": [
        #                     "voice"
        #                 ]
        #             },
        #             {
        #                 "id": 15,
        #                 "label": "Color",
        #                 "value": 20,
        #                 "desc": "the color in the img, which include image, foreground and background color",
        #                 "categories": [
        #                     "info"
        #                 ]
        #             },
        #             {
        #                 "id": 16,
        #                 "label": "Evaluate",
        #                 "value": 20,
        #                 "desc": "some values to evaluate the img, like total view, total likes, total click, etc.",
        #                 "categories": [
        #                     "info"
        #                 ]
        #             },
        #             {
        #                 "id": 17,
        #                 "label": "Date",
        #                 "value": 20,
        #                 "desc": "date based on month, you could filter all the memories in a certain month",
        #                 "categories": [
        #                     "date"
        #                 ]
        #             },
        #             {
        #                 "id": 18,
        #                 "label": "Address",
        #                 "value": 20,
        #                 "desc": "based on city, you could filter all the memories that happened in this city",
        #                 "categories": [
        #                     "location"
        #                 ]
        #             },
        #             {
        #                 "id": 19,
        #                 "label": "Mcs",
        #                 "value": 20,
        #                 "desc": "Multi-chain storage based on the web3 concept, keep your date more safe",
        #                 "categories": [
        #                     "info"
        #                 ]
        #             },
        #             {
        #                 "id": 20,
        #                 "label": "Tag",
        #                 "value": 20,
        #                 "desc": "add some tags to some nodes like Img, Event, etc.",
        #                 "categories": [
        #                     "info"
        #                 ]
        #             },
        #         ],
        #         "edges": [
        #             {
        #                 "from": 1,
        #                 "to": 2,
        #                 "label": "inherit"
        #             },
        #             {
        #                 "from": 2,
        #                 "to": 3,
        #                 "label": "work in"
        #             },
        #
        #             {
        #                 "from": 2,
        #                 "to": 4,
        #                 "label": "own"
        #             },
        #             {
        #                 "from": 2,
        #                 "to": 5,
        #                 "label": "provide"
        #             },
        #             {
        #                 "from": 2,
        #                 "to": 6,
        #                 "label": "need"
        #             },
        #             {
        #                 "from": 2,
        #                 "to": 7,
        #                 "label": "join in"
        #             },
        #             {
        #                 "from": 2,
        #                 "to": 11,
        #                 "label": "face info"
        #             },
        #             {
        #                 "from": 2,
        #                 "to": 9,
        #                 "label": "own"
        #             },
        #             {
        #                 "from": 4,
        #                 "to": 3,
        #                 "label": "experience in"
        #             },
        #             {
        #                 "from": 4,
        #                 "to": 9,
        #                 "label": "include"
        #             },
        #
        #             {
        #                 "from": 5,
        #                 "to": 9,
        #                 "label": "include"
        #             },
        #             {
        #                 "from": 6,
        #                 "to": 9,
        #                 "label": "include"
        #             },
        #             {
        #                 "from": 7,
        #                 "to": 9,
        #                 "label": "memory"
        #             },
        #             {
        #                 "from": 7,
        #                 "to": 13,
        #                 "label": "memory"
        #             },
        #             {
        #                 "from": 7,
        #                 "to": 14,
        #                 "label": "memory"
        #             },
        #             {
        #                 "from": 7,
        #                 "to": 20,
        #                 "label": "include"
        #             },
        #             {
        #                 "from": 8,
        #                 "to": 10,
        #                 "label": "record in "
        #             },
        #             {
        #                 "from": 9,
        #                 "to": 8,
        #                 "label": "belongs to "
        #             },
        #             {
        #                 "from": 9,
        #                 "to": 10,
        #                 "label": "record in"
        #             },
        #             {
        #                 "from": 9,
        #                 "to": 11,
        #                 "label": "belongs to "
        #             },
        #             {
        #                 "from": 9,
        #                 "to": 12,
        #                 "label": "have faces"
        #             },
        #
        #             {
        #                 "from": 9,
        #                 "to": 15,
        #                 "label": "include"
        #             },
        #             {
        #                 "from": 9,
        #                 "to": 16,
        #                 "label": "include "
        #             },
        #             {
        #                 "from": 9,
        #                 "to": 17,
        #                 "label": "token on"
        #             },
        #             {
        #                 "from": 9,
        #                 "to": 18,
        #                 "label": "located in"
        #             },
        #             {
        #                 "from": 9,
        #                 "to": 19,
        #                 "label": "include"
        #             },
        #             {
        #                 "from": 9,
        #                 "to": 20,
        #                 "label": "include"
        #             },
        #             {
        #                 "from": 9,
        #                 "to": 12,
        #                 "label": "have faces"
        #             },
        #             {
        #                 "from": 9,
        #                 "to": 8,
        #                 "label": "belongs to "
        #             },
        #             {
        #                 "from": 9,
        #                 "to": 10,
        #                 "label": "record in"
        #             },
        #             {
        #                 "from": 9,
        #                 "to": 11,
        #                 "label": "belongs to "
        #             },
        #             {
        #                 "from": 9,
        #                 "to": 12,
        #                 "label": "have faces"
        #             },
        #             {
        #                 "from": 11,
        #                 "to": 12,
        #                 "label": "have faces "
        #             },
        #             {
        #                 "from": 13,
        #                 "to": 20,
        #                 "label": "include"
        #             },
        #             {
        #                 "from": 14,
        #                 "to": 20,
        #                 "label": "include"
        #             },
        #
        #         ]
        #     }
        # }
        return Response(graph)

    def get_relation_of_img_profile(self):
        # faces = Face.objects.filter(profile__isnull=False)
        faces = Face.objects.select_related('img', 'profile').filter(profile__isnull=False)
        edges = [{
            "from": face.img_id,
            "to": face.profile_id,
            "label": "include"}
            for face in faces]
        return edges

class ImgMcsViewSet(viewsets.ModelViewSet):
    queryset = ImgMcs.objects.all().order_by('-id')
    serializer_class = McsSerializer
    # permission_classes = (AllowAny,)
    pagination_class = GalleryPageNumberPagination  # could disp the filter button in the web


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().annotate(value=Count('imgs')).order_by('-value')  # ordered by the
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
            'fc_nums': Img.get_attr_nums('faces'),
            'fc_name': Profile.get_attr_nums('face_imgs'),

            'tags': Tag.objects.annotate(value=Count('imgs')).filter(value__gt=0).order_by('-value').values('name',
                                                                                                            'value'),

            'c_img': [{**item, 'color': calib['color_palette'][item['name']]} for item in Category.get_cate_children(name='img_color')],
            'c_back': [],
            'c_fore': [],

            # 'scene': Category.get_cate_children(name='scene'), # TODO: haven't done yet
            'scene': Category.get_cate_children(name='scene'),
            'group': Category.get_cate_children(name='group'),
            'country': Category.get_cate_children(name='location', level=1),
            'province': Category.get_cate_children(name='location', level=2),
            'city': Category.get_cate_children(name='location', level=3),
            # 'city': Category.get_cate_children_loop('location', level=0).annotate(value=Count('imgs')).values('name',
            #                                                                                                      'value').distinct().order_by(
            # '-value'),
            'layout': Category.get_cate_children(name='layout'),
            'size': Category.get_cate_children(name='size'),
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

    def get_queryset(self):
        if self.action == 'list':
            # only return the root category
            return Category.objects.filter(is_root=True).annotate(value=Count('imgs')).order_by('-value')
        else:
            # return all the category
            return self.queryset


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
    filter_class = FaceFilter  # 过滤类
    # serializer_class = FaceBriefSerializer
    # permission_classes = (AllowAny,)
    # pagination_class = FacePageNumberPagination  # 增加了这句代码，就无法显示filter,不过效果还是有的

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  # 模糊过滤，注意的是，这里的url参数名变成了?search=搜索内容
    # filterset_fields = ['profile__id', 'img__id']  # 外键需要增加2个下划线
    # # filterset_fields = ['img', 'name', 'is_confirmed', 'face_score']
    # search_fields = ['profile__id', 'img__id']
    # ordering_fields = ['img__id']  # 这里的字段，需要总上面定义字段中选择


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
