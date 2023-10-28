import json
import os.path
from io import BytesIO

import cv2
import numpy as np
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from taggit.models import Tag

from deep_diary.settings import calib, cfg
from library.filters import ImgFilter, CategoryFilter, AddressFilter, FaceFilter, search_fields_face, search_fields_img
from library.models import Img, Category, Address, Stat, Evaluate, Date, ImgMcs, Face
from library.pagination import GalleryPageNumberPagination, AddressNumberPagination, FacePageNumberPagination
from library.serializers import ImgSerializer, ImgDetailSerializer, ImgCategorySerializer, McsSerializer, \
    CategorySerializer, AddressSerializer, CategoryDetailSerializer, FaceSerializer, FaceBriefSerializer
from library.serializers_out import CategoryBriefSerializer, ImgGraphSerializer, CategoryFilterListSerializer, \
    FaceGraphSerializer
from library.task import ImgProces, check_img_info, check_all_img_info
from user_info.models import Profile, ReContact, relation_strings, RELATION_OPTION, Experience, Company
from user_info.serializers_out import ProfileGraphSerializer, ProfileBriefSerializer, ReContactGraphSerializer, \
    ExperienceGraphSerializer, CompanyGraphSerializer
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
    queryset = Img.objects.all()

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

    search_fields = search_fields_img

    ordering_fields = ['id', 'dates__capture_date']  # 这里的字段，需要总上面定义字段中选择

    def perform_create(self, serializer):
        print(f"INFO:Img start perform_create, {self.request.user}")
        print(f"INFO:Img file, {self.request.FILES}")
        file = self.request.FILES.get("src")
        f_path = file.temporary_file_path()
        print(f"INFO:temporary_file_path, {f_path}")

        instance = serializer.save(user=self.request.user)
        check_img_info.delay(instance)

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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # ------------------------------------------------------------------------------
        """Entity Recognition"""
        """NLP Search"""
        if cfg["img"]["enable_nlp_search"]:  # 是否开启NLP search
            search_param = request.query_params.get('search', '').replace('\x00', '')  # strip null characters
            if search_param:
                norm_len = len(queryset)
                print('search_param is enabled: ', search_param)
                search_queryset = ImgProces.img_recognition(search_param)
                print('search_result is: ', len(search_queryset))

                # 将自然语言搜索跟原始搜索进行合并
                if norm_len > 0:
                    queryset = search_queryset.union(queryset)
                    ids = [qs.id for qs in queryset]
                    queryset = Img.objects.filter(id__in=ids)
                else:
                    queryset = search_queryset
        # ------------------------------------------------------------------------------

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
            get_list = cfg["img"]["process_list"]
        if add_list_org == 'all':
            print('INFO:-> add_list_org == all')
            add_list = cfg["img"]["add_list"]
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

        # img_process = ImgProces()
        # img_process.get_all_img(img_process, func_list=get_list, force=force)
        # img_process.add_all_img_to_category(img_process, func_list=add_list)

        check_all_img_info.delay(get_list=get_list, add_list=add_list, force=force)
        return Response({"msg": "batch_img_test success"})

    @action(detail=True, methods=['get'])  # 在详情中才能使用这个自定义动作
    def img_process(self, request, pk=None):  # 当detail=True 的时候，需要指定第三个参数，如果未指定look_up, 默认值为pk，如果指定，该值为loop_up的值
        print('------------------img_process------------------')
        instance = self.get_object()  # 获取详情的实例对象
        force, get_list, add_list = self.img_pre_process()

        # img_process = ImgProces(instance=instance)
        # if get_list:
        #     print(f'INFO:-> param get_list: {get_list}')
        #     img_process.get_img.delay(img_process, instance=instance, func_list=get_list, force=force)
        # if add_list:
        #     print(f'INFO:-> param add_list: {add_list}')
        #     img_process.add_img_to_category.delay(img_process, instance=instance, func_list=add_list)
        #
        # print('------------------img_process finished------------------')

        check_img_info(instance=instance, get_list=get_list, add_list=add_list, force=force)
        return Response({"msg": 'img_process finished'})

    @action(detail=False, methods=['get'])  # will be used in the list view since the detail = false
    def upload_finished(self, request, pk=None):
        print('------------------upload_finished------------------')

        # TODO do something after uploading the image
        data = {
            "data": '',
            'code': 200,
            'msg': 'All the images have been uploaded successfully'
        }
        return Response(data)

    @action(detail=False, methods=['get'])  # will be used in the list view since the detail = false
    def get_filtered_list(self, request, pk=None):
        search_param = request.query_params.get('search', '').replace('\x00', '')  # strip null characters
        # if search in one search model, then skip filter the filter list
        if search_param:
            qs = self.get_queryset()
        else:
            qs = self.filter_queryset(self.get_queryset())

        queryset = qs
        # ------------------------------------------------------------------------------
        """Entity Recognition"""
        """NLP Search"""
        if cfg["img"]["enable_nlp_search"]:  # 是否开启NLP search
            if search_param:
                norm_len = len(queryset)
                print('search_param is enabled: ', search_param)
                search_queryset = ImgProces.img_recognition(search_param)
                print('search_result is: ', len(search_queryset))

                # 将自然语言搜索跟原始搜索进行合并
                if norm_len > 0:
                    queryset = search_queryset.union(queryset)
                    ids = [qs.id for qs in queryset]
                    queryset = Img.objects.filter(id__in=ids)
                else:
                    queryset = search_queryset

        # ------------------------------------------------------------------------------

        # 2. 统计每个Profile在img_queryset出现的次数，记作value
        profile_list = Profile.objects.exclude(name__startswith='unknown').filter(
            face_imgs__in=queryset
        ).annotate(value=Count('face_imgs')).distinct().values('name', 'value').order_by('-value')

        #

        # 判断是否存在categories.json文件，如果存在，则读取，如果不存在，则生成
        if os.path.exists('categories.json'):
            with open('categories.json', 'r') as f:
                categories = json.load(f)
        else:
            # TODO , 如下的serializer，返回的是全部结果，并非基于查询集的结果 , imgs__in=queryset
            categories = Category.objects.filter(is_root=True).distinct()  # 这里不加.distinct()巨慢无比
            serializer = CategoryFilterListSerializer(categories, many=True, context={'imgs': queryset})
            categories = serializer.data
            # categories 是json格式的数据，将其保存到本地
            with open('categories.json', 'w') as f:
                json.dump(categories, f)

        #
        data = {
            'categories': categories,
            'fc_nums': Img.get_filtered_attr_nums(queryset, 'faces'),  # 这张照片包含的人脸数量
            'fc_name': profile_list,

            'tags': Tag.objects.filter(imgs__in=queryset).annotate(value=Count('imgs')).distinct().order_by(
                '-value').values('name',
                                 'value'),

            'c_img': [{**item, 'color': calib['color_palette'][item['name']]} for item in
                      Category.get_filtered_cate_children(queryset, name='img_color')],
            # 'c_back': [],
            # 'c_fore': [],
            'scene': Category.get_filtered_cate_children(queryset, name='scene'),
            'classification': Category.get_filtered_cate_children(queryset, name='clip_categories'),
            'group': Category.get_filtered_cate_children(queryset, name='group'),  # the queryset represent the imgs

            # 'country': set(queryset.exclude(address__country__isnull=True).values_list('address__country', flat=True)),
            # 'province': set(queryset.exclude(address__province__isnull=True).values_list('address__province', flat=True)),
            'city': set(
                queryset.exclude(address__city__isnull=True).exclude(address__city='[]').values_list('address__city',
                                                                                                     flat=True)),

            #
            # 'country': Category.get_filtered_cate_children(queryset, name='location', level=1),
            # 'province': Category.get_filtered_cate_children(queryset, name='location', level=2),
            # 'city': Category.get_filtered_cate_children(queryset, name='location', level=3),

            # 'layout': Category.get_filtered_cate_children(queryset, name='layout'),
            'layout': ['Tall', 'Wide', 'Square'],
            # 'size': Category.get_filtered_cate_children(queryset, name='size'),
            # 'license': ['Public domain', 'Free to share and use', 'Free to share and use commercially'],
            'ordering': ['id', '-id', 'dates__capture_date', '-dates__capture_date']

        }

        # data['tags'] = list(data['tags'])
        # data['tags'].insert(0, 'All')
        # # 循环判断是否有all字段，如果没有，则转换成列表并插入
        return Response({
            'msg': 'success to get_filtered_list',
            'code': 200,
            'data': data,
        })

        # return Response({
        #     'msg': 'success to get_filtered_list',
        #     'code': 200,
        #     # 'data': data,
        # })

    @action(detail=False, methods=['get'])  # 在详情中才能使用这个自定义动作
    def graph(self, request, pk=None):  # 当detail=True 的时候，需要指定第三个参数，如果未指定look_up, 默认值为pk，如果指定，该值为loop_up的值

        # get the original id
        node_img = ImgGraphSerializer(self.queryset.filter(faces__isnull=False), many=True,
                                      context={'request': request}).data
        node_profile = ProfileGraphSerializer(Profile.objects.all(), many=True,
                                              context={'request': request}).data  # 这里需要传入查询集
        node_company = CompanyGraphSerializer(Company.objects.all(), many=True).data

        edges_img_profile = FaceGraphSerializer(Face.objects.filter(profile__isnull=False), many=True).data
        edges_profile_profile = ReContactGraphSerializer(ReContact.objects.all(), many=True).data
        edges_profile_company = ExperienceGraphSerializer(Experience.objects.all(), many=True).data

        # update the related id based on model name
        node_img = self.update_graph_node_id(node_img, 'img')
        node_profile = self.update_graph_node_id(node_profile, 'profile')
        node_company = self.update_graph_node_id(node_company, 'company')

        edges_img_profile = self.update_graph_edge_id(edges_img_profile, 'img', 'profile')
        edges_profile_profile = self.update_graph_edge_id(edges_profile_profile, 'profile', 'profile')
        edges_profile_company = self.update_graph_edge_id(edges_profile_company, 'profile', 'company')

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
                "nodes": node_img +
                         node_profile +
                         node_company,
                "edges": edges_img_profile +
                         edges_profile_profile +
                         edges_profile_company
            }
        }

        return Response(graph)

    @staticmethod
    def update_graph_node_id(nodes, prefix):
        """
        目的： 考虑到不同模块节点的id可能会一样，因此需要更新图谱中的id，将原来的id替换成新的id， 可以实现模块前缀+id的形式
              e.g. img node 中有 id = 1， profile中也有id= 1, 那对应的edge中的from_id 和 to_id 都需要更新
        param: nodes:更新前的 nodes 列表
        param: prefix: 模块前缀
        return: nodes 更新后的nodes
        example: nodes = self.update_graph_node_id(nodes, prefix='img')
        """
        # nodes_updated = [{'id': prefix + str(node['id']), **node} for node in nodes]
        nodes_updated = [{**node, 'id': prefix + str(node['id'])} for node in nodes]  # 改动的需要在后面，不然会被后面覆盖

        return nodes_updated

    @staticmethod
    def update_graph_edge_id(edges, prefix_from, prefix_to):
        """
        目的： 考虑到不同模块节点的id可能会一样，因此需要更新图谱中的id，将原来的id替换成新的id， 可以实现模块前缀+id的形式
              e.g. img node 中有 id = 1， profile中也有id= 1, 那对应的edge中的from_id 和 to_id 都需要更新
        param: edges:更新前的edges 列表
        param: prefix_from: from模块前缀
        param: prefix_to: to模块前缀
        return: edge 更新后的edge
        example: node = self.update_graph_edge_id(edge, 'img', 'profile')
        """
        # 改动的需要在后面，不然会被后面覆盖
        edges = [{**edge, 'from': prefix_from + str(edge['from']), 'to': prefix_to + str(edge['to'])} for edge in edges]

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

            'c_img': [{**item, 'color': calib['color_palette'][item['name']]} for item in
                      Category.get_cate_children(name='img_color')],
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
            return CategoryBriefSerializer  # CategoryBriefSerializer， CategoryFilterListSerializer
        else:
            return CategorySerializer

    def get_queryset(self):
        if self.action == 'list':
            # only return the root category
            return self.queryset
            # return Category.objects.filter(is_root=True).annotate(value=Count('imgs')).order_by('-value')
            # return Category.objects.all()
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

    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]  # 模糊过滤，注意的是，这里的url参数名变成了?search=搜索内容

    search_fields = search_fields_face

    # ordering_fields = ['img__id']  # 这里的字段，需要总上面定义字段中选择

    def perform_update(self, serializer):  # 应该在调用的模型中添加
        print(f'人脸更新：validated_data =  {serializer.validated_data}')
        print(f'人脸更新：validated_data =  {self.request.data.get("name", None)}')
        print(f'当前访问人脸的用户是 =  {self.request.user}')

        fc = self.get_object()
        process = ImgProces()
        profile, fc_instance = process.face_rename(fc, self.request.data.get('name', None))
        serializer.validated_data["profile"] = profile
        serializer.save()  # 保存更新的实例对象

    def get_serializer_class(self):
        if self.action == 'list':
            print(self.action)
            return FaceBriefSerializer
        else:
            return FaceSerializer

    # TODO: combine the following function with the original function   filter_queryset
    # def filter_queryset(self, queryset):
    #     qs=self.get_queryset()
    #     print(len(qs))
    #     def get_search_terms(request):
    #         """
    #         Search terms are set by a ?search=... query parameter,
    #         and may be comma and/or whitespace delimited.
    #         """
    #         params = request.query_params.get('search', '')
    #         params = params.replace('\x00', '')  # strip null characters
    #         params = params.replace(',', ' ')
    #         return params.split()
    #
    #     search_param = get_search_terms(self.request)
    #     print('search_param: ', search_param)
    #     if search_param:
    #         # 在这里执行根据 choices 中的字符串值进行搜索的逻辑
    #         re_list = [choice[0] for choice in RELATION_OPTION if choice[1] in search_param]
    #         print('re_list: ', re_list)
    #         qs = qs.filter(profile__re_from_relations__relation__in=re_list).distinct() if re_list else qs
    #     print(len(qs))
    #
    #     # queryset = super().filter_queryset(qs)
    #     queryset = qs
    #
    #     return queryset

    @action(detail=False, methods=['get'])  # will be used in the list view since the detail = false
    def get_filtered_list(self, request, pk=None):
        user = self.request.user  # 获取当前登录用户的实例
        # qs = self.filter_queryset(self.get_queryset())
        #
        # queryset = qs

        related_str = []
        # 获取跟当前用户相关的人脸
        if user.is_authenticated:
            print('user is authenticated: ', user.name)
            # 如下的relation ,得到的数字，期望得到对应的字符串
            # related = user.re_to_relations.all()
            # related_str=[relation_strings[item.relation] for item in related]
            # related_str = set(related_str)

            related_id = user.re_to_relations.all().values_list('relation', flat=True)
            related_str = [relation_strings[id] for id in set(related_id)]

            print('related_str: ', related_str)

            # queryset = queryset.filter(profile__re_to_relations__owner=user)
        else:
            print('user is not authenticated')
            # queryset = queryset.filter(profile__recontact__owner__isnull=True)

        # 2. 统计每个Profile在img_queryset出现的次数，记作value
        profile_list = (Profile.objects.annotate(value=Count('faces'))
                        .distinct().values('name', 'value').order_by('-value'))

        data = {
            'confirmed': [
                {'name': 'Unconfirmed', 'value': 0},
                {'name': 'Confirmed', 'value': 1},
            ],
            'profile__name': profile_list,
            'profile__isnull': [
                {'name': 'Has Related Profile', 'value': 0},
                {'name': 'No Related Profile', 'value': 1},
            ],
            'det_score__gt': [0.9, 0.8, 0.7, 0.6, 0.5],
            'det_score__lt': [0.4, 0.5, 0.6, 0.7, 0.8],
            'face_score__gt': [0.9, 0.8, 0.7, 0.6, 0.5],
            'face_score__lt': [0.4, 0.5, 0.6, 0.7, 0.8],
            'gender': [
                {'name': 'Female', 'value': 0},
                {'name': 'Male', 'value': 1},  # logical of insightface
            ],
            'pose_x__gt': [-20, -10, 0, 10, 20],
            'pose_x__lt': [-20, -10, 0, 10, 20],
            'pose_y__gt': [-20, -10, 0, 10, 20],
            'pose_y__lt': [-20, -10, 0, 10, 20],
            'pose_z__gt': [-20, -10, 0, 10, 20],
            'pose_z__lt': [-20, -10, 0, 10, 20],
            'wid__gt': [1000, 800, 600, 400, 200],
            'wid__lt': [1000, 800, 600, 400, 200],
            'state': [
                {'name': 'Normal', 'value': 0},
                {'name': 'Forbidden', 'value': 1},
                {'name': 'Deleted', 'value': 9},
            ],
            'relation': related_str,

        }

        return Response({
            'msg': 'success to get the face filter list',
            'code': 200,
            'data': data,
        })
