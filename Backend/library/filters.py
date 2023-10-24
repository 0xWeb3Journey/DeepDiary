from functools import reduce
from operator import and_

from django.db.models import Count, Q, Prefetch
from django_filters import rest_framework
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework import filters
from taggit.managers import TaggableManager
from taggit.models import Tag

from library.models import Img, Category, Address, Face
from django.db import models
import django_filters

from user_info.models import Profile, string_to_int_mapping, ReContact

# only for text search
search_fields_img = {
    'id': ['exact', 'gte', 'lte'],
    # color
    'colors__image__closest_palette_color_parent': ['exact'],

    # category
    'categories__name': ['exact'],  #
    # address
    'address__country': ['exact', 'contains'],
    'address__province': ['exact', 'contains'],
    'address__city': ['exact', 'contains'],
    'address__district': ['exact', 'contains'],
    'address__location': ['icontains'],
    # profile
    'user__name': ['exact'],  #
    'user__username': ['exact'],  #
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

# only for text search
search_fields_face = {
    'profile__id': ['exact'],  #
    'profile__name': ['exact', 'icontains'],
    'profile__full_pinyin': ['exact', 'icontains'],
    'profile__lazy_pinyin': ['exact', 'icontains'],
    'profile__companies__name': ['exact', 'icontains'],
    'profile__companies__name_PyFull': ['exact', 'icontains'],
    'profile__companies__name_PyInitial': ['exact', 'icontains'],
}


class TagsFilter(django_filters.CharFilter):

    def filter(self, qs, value):
        if value:
            tags = [tag.strip() for tag in value.split(',')]  # strip()去除首尾空格， string to list
            print(tags)
            # qs = qs.filter(tags__name__in=tags).distinct()  # through or logical
            for tag in tags:  # through and logical, filter for several times
                qs = qs.filter(tags__name=tag)

        return qs.distinct()


class FaceFilter(FilterSet):
    relation = django_filters.CharFilter('profile', method='relation_filter')
    confirmed = django_filters.CharFilter('profile', method='confirmed_filter')

    class Meta:
        model = Face  # 模型名

        fields = {

            'profile__id': ['exact'],  #
            'profile__name': ['exact', 'icontains'],
            'profile__re_to_relations__relation': ['exact'],
            'profile': ['exact', 'isnull'],  #
            'det_score': ['gt', 'lt'],
            'face_score': ['gt', 'lt'],  #
            'age': ['gt', 'lt'],
            'gender': ['exact'],
            'pose_x': ['gt', 'lt'],
            'pose_y': ['gt', 'lt'],
            'pose_z': ['gt', 'lt'],
            'wid': ['gt', 'lt'],
            'state': ['exact'],
        }

    def relation_filter(self, qs, name, value):
        relation = string_to_int_mapping.get(value, None)
        user = self.request.user

        if not relation:
            return qs
        print('relation_filter: ', name, value, relation)
        # find the profile ids based on the relation string
        profile_ids = ReContact.objects.filter(relation=relation, re_to=user).values_list('re_from', flat=True)
        print(profile_ids)
        # filter the related faces based on the profile ids
        qs = qs.filter(profile__id__in=profile_ids)

        return qs

    def confirmed_filter(self, qs, name, value):
        print('confirmed_filter: ', name, value)
        # 去掉那些name以'unknown'开头的记录
        if value == '1':
            print('confirmed_filter: exclude the unknown profile', name, value)
            qs = qs.exclude(profile__name__startswith='unknown')
        elif value == '0':
            print('confirmed_filter: include the unknown profile', name, value)
            qs = qs.filter(profile__name__startswith='unknown')
        else:
            qs = qs

        return qs

    # def filter(self, qs, value):
    #     print(f'the value in FacesFilter is {qs}, value is {value}')
    #     if value is None:
    #         qs = qs
    #     elif value <= 6:
    #         qs = qs.annotate(fc_nums=Count('faces')).filter(fc_nums=value)
    #     else:
    #         qs = qs.annotate(fc_nums=Count('faces')).filter(fc_nums__gte=value)
    #     return qs


class CategoryFilter(FilterSet):
    family = django_filters.CharFilter('name', method='filter_family')
    ancestors = django_filters.CharFilter('name', method='filter_ancestors')
    siblings = django_filters.CharFilter('name', method='filter_siblings')
    children = django_filters.CharFilter('name', method='filter_children')
    descendants = django_filters.CharFilter('name', method='filter_descendants')

    class Meta:
        model = Category  # 模型名

        fields = {
            # color
            'name': ['exact', 'icontains'],
            'parent__name': ['exact', 'icontains'],
            'is_leaf': ['exact'],
            'is_root': ['exact'],
            'owner': ['exact'],
        }

    # 自定义方法
    def filter_children(self, qs, name, value):
        print('INFO: filter_children--> start---------', name, value, type(value))
        if value:
            qs = qs.filter(
                name=value).first().get_children()  # .annotate(value=Count('imgs')).distinct().order_by('-value')
        return qs

    def filter_family(self, qs, name, value):
        print('INFO: filter_family--> start---------', name, value, type(value))
        if value:
            qs = qs.filter(
                name=value).first().get_family()  # .annotate(value=Count('imgs')).distinct().order_by('-value')
        return qs

    def filter_descendants(self, qs, name, value):
        print('INFO: filter_descendants--> start---------', name, value, type(value))
        if value:
            qs = qs.filter(
                name=value).first().get_descendants(include_self=False) # .annotate(value=Count('imgs')).distinct().order_by('-value')
        return qs

    def filter_siblings(self, qs, name, value):
        print('INFO: filter_siblings--> start---------', name, value, type(value))
        if value:
            qs = qs.filter(
                name=value).first().get_siblings(include_self=True) # .annotate(value=Count('imgs')).distinct().order_by('-value')
        return qs

    def filter_ancestors(self, qs, name, value):
        print('INFO: filter_ancestors--> start---------', name, value, type(value))
        if value:
            qs = qs.filter(
                name=value).first().get_ancestors(ascending=False, include_self=False) # .annotate(value=Count('imgs')).distinct().order_by('-value')
        return qs


class ImgFilter(FilterSet):
    categories = django_filters.CharFilter('categories', method='filter_categories')

    tags = TagsFilter(field_name="tags", method='filter_tags')  # method 1
    # tags = django_filters.CharFilter('tags', method='filter_tags')  # method 2

    # color
    c_img = django_filters.CharFilter('colors', method='filter_img_colors')
    c_fore = django_filters.CharFilter('colors', method='filter_fore_colors')
    c_back = django_filters.CharFilter('colors', method='filter_back_colors')

    # faces
    # faces = FacesFilter()
    fc_nums = django_filters.NumberFilter('faces', method='filter_fc_nums')
    fc_name = django_filters.CharFilter('faces', method='filter_fc_name')

    layout = django_filters.CharFilter('aspect_ratio', method='filter_layout')

    class Meta:
        model = Img  # 模型名

        fields = {
            # 'id': ['exact', 'gte', 'lte'],
            # color
            'colors__image__closest_palette_color_parent': ['exact', 'icontains'],
            'colors__foreground__closest_palette_color_parent': ['exact', 'icontains'],
            'colors__background__closest_palette_color_parent': ['exact', 'icontains'],
            # category
            'categories__name': ['exact'],  #
            # 'categories__type': ['exact'],  #
            # 'categories__value': ['exact'],  #
            # address
            'address__is_located': ['exact'],
            'address__country': ['exact', 'contains'],
            'address__province': ['exact', 'contains'],
            'address__city': ['exact', 'contains'],
            'address__district': ['exact', 'contains'],
            'address__location': ['icontains'],
            'address__longitude': ['gte', 'lte', 'range'],
            'address__latitude': ['gte', 'lte', 'range'],
            # user
            'user__name': ['exact'],  #
            'user__username': ['exact'],  #
            # date
            'dates__year': ['exact', 'gte', 'lte', 'contains'],  #
            'dates__month': ['exact', 'gte', 'lte', 'contains'],  #
            'dates__day': ['exact', 'gte', 'lte', 'contains', 'isnull'],  #
            'dates__capture_date': ['exact', 'gte', 'lte', 'contains', 'isnull', 'range'],
            # http://127.0.0.1:8000/api/img/?dates__capture_date__isnull=true
            # evaluates
            'evaluates__rating': ['exact'],  #
            'evaluates__flag': ['exact'],  #
            'evaluates__total_views': ['exact', 'gte', 'lte'],  #
            'evaluates__likes': ['exact', 'gte', 'lte'],  #
            # tags
            'tags': ['exact', 'icontains'],  #
            'tags__name': ['exact', 'icontains'],  #
            # img
            'name': ['exact', 'icontains'],  #
            'title': ['exact', 'icontains'],  #
            'caption': ['exact', 'icontains'],  #
            "type": ['exact'],
            "wid": ['exact', 'gte', 'lte'],
            "height": ['exact', 'gte', 'lte'],
            "aspect_ratio": ['exact', 'gte', 'lte'],  # need to change to float type
            # "is_publish": ['exact'],
        }

        filter_overrides = {
            TaggableManager: {  # unrecognized field type TaggableManager, so must be overrides
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'name__icontains',  # here we're saying to look through the icontains prop on name
                },
            },

        }

    def filter_tags(self, queryset, name, value):
        if value:
            tags = [tag.strip() for tag in value.split(',')]  # strip()去除首尾空格

            # 方法一：通过filter实现
            for item in tags:
                queryset = queryset.filter(tags__name=item)

            # Prefetch the related tags for each image---> TaggableManager 不支持这个方法
            # queryset = queryset.prefetch_related(Prefetch('tags', queryset=Tag.objects.filter(name__in=tags)))

            queryset = queryset.distinct()

            # 方法二：通过Q对象实现, TODO: 有问题，待解决, 可能是TaggableManager的问题
            # q_tags = Q()
            # q_tags.connector = 'OR'
            # for item in tags:
            #     q_tags.children.append(('tags__name', item))
            # # q_tags = reduce(and_, (Q(tags__name=item) for item in tags))  # Use reduce to combine Q objects with AND operator
            # print(q_tags)
            # queryset = queryset.filter(q_tags).distinct()

        return queryset

    def filter_categories(self, queryset, name, value):
        print('INFO: filter_categories--> start---------', name, value, type(value))
        if value:
            categories = [cate.strip() for cate in value.split(',')]  # strip()去除首尾空格

            # 方法一：通过filter实现
            for item in categories:
                # print('INFO: filter_categories-->', item, len(queryset))
                queryset = queryset.filter(categories__name=item)

            queryset = queryset.distinct()

        return queryset

    def filter_fc_nums(self, qs, name, value):
        if value is not None and value >= 0:
            qs = qs.annotate(fc_nums=Count('faces')).filter(fc_nums=value).distinct()
        return qs

    def filter_fc_name(self, qs, name, value):
        if value:
            names = [name.strip() for name in value.split(',')]
            # q_names = Q()
            # q_names.connector = 'AND'
            # for item in names:
            #     q_names.children.append(('profiles__name', item))

            # q_names = Q(profiles__name__in=names)
            # qs = qs.filter(q_names).distinct()
            # print(q_names)

            # 通过Prefetch实现, 理论上会更快，但可能数据量过小，还未进行验证，目前这句话加不加，感觉差不多，加了查询次数反而更大
            qs = qs.prefetch_related(Prefetch('profiles', queryset=Profile.objects.filter(name__in=names)))
            for item in names:
                qs = qs.filter(profiles__name=item)
            qs.distinct()

        return qs

    def filter_img_colors(self, qs, name, value):
        #
        # print(name)

        if value:
            names = [name.strip() for name in value.split(',')]  # strip()去除首尾空格
            # qs = qs.select_related('colors').filter(colors__image__closest_palette_color_parent__in=names)
            print(f'filter_image_colors--> the original qs count is  {qs.count()} before filter, names is {names} ')
            for item in names:  # through and logical
                qs = qs.filter(colors__image__closest_palette_color_parent=item)
            qs = qs.distinct()
        print(f'filter_image_colors--> the original qs count is  {qs.count()}')
        return qs

    def filter_fore_colors(self, qs, name, value):

        if value:
            names = [name.strip() for name in value.split(',')]  # strip()去除首尾空格
            print(names)
            # qs = qs.select_related('colors').filter(colors__foreground__closest_palette_color_parent__in=names)
            for item in names:  # through and logical
                qs = qs.filter(colors__foreground__closest_palette_color_html_code=item)
            qs = qs.distinct()

        # print(f'filter_fore_colors--> the original qs count is  {qs.count()}')
        return qs

    def filter_back_colors(self, qs, name, value):

        # print(name)
        # print(value)
        if value:
            names = [name.strip() for name in value.split(',')]  # strip()去除首尾空格

            # 通过Prefetch实现, 理论上会更快，但可能数据量过小，还未进行验证，目前这句话加不加，感觉差不多，加了查询次数反而更大
            # qs = qs.select_related('colors').filter(colors__background__closest_palette_color_parent__in=names)
            for item in names:  # through and logical
                qs = qs.filter(colors__background__closest_palette_color_html_code=item)
            qs = qs.distinct()

        # print(f'filter_back_colors--> the original qs count is {qs.count()}')
        return qs

    def filter_layout(self, qs, name, value):
        if value == 'Square':
            qs = qs.filter(aspect_ratio=1)
        elif value == 'Wide':
            qs = qs.filter(aspect_ratio__lt=1)
        elif value == 'Tall':
            qs = qs.filter(aspect_ratio__gt=1)
        print('filter_layout', name, value)
        return qs


class ImgSearchFilter(filters.SearchFilter):
    class Meta:
        model = Img  # 模型名

        fields = {
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

    def get_search_fields(self, view, request):
        if request.query_params.get('title_only'):
            return ['title']
        return super(ImgSearchFilter, self).get_search_fields(view, request)


class AddressFilter(FilterSet):
    class Meta:
        model = Address  # 模型名

        fields = {
            # if searching with contains or icontains, should do like this: address__is_located__contains = **
            'is_located': ['exact'],
            'country': ['exact', 'contains'],
            'province': ['exact', 'contains'],
            'city': ['exact', 'contains', 'isnull'],
            'district': ['exact', 'contains'],
            'location': ['icontains'],
            'longitude': ['gte', 'lte', 'range'],
            'latitude': ['gte', 'lte', 'range'],
        }
