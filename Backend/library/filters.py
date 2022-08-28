from django_filters import rest_framework
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework import filters
from library.models import Img
from django.db import models
import django_filters
# class TagsFilter(filters.CharFilter):
#     def filter(self, qs, value):
#         if value:
#             tags = [tag.strip() for tag in value.split(',')]   # strip()去除首尾空格
#             print(tags)
#             # qs = qs.filter(tags__name__in=tags).distinct()
#             for tag in tags:
#                 qs = qs.filter(tags__name=tag).distinct()
#
#         return qs

#
# class TaggableModelFilterSet(FilterSet):
#
#     tags = TagsFilter()
#
#     class Meta:
#         model = Img
#         fields = ['year', 'month', 'day', 'tags']
#         # fields = {
#         #     'year': ['exact', 'contains'],
#         #     'month': ['exact', 'contains'],
#         #     'day': ['exact', 'contains'],
#         #     'tags': ['exact', 'contains'],
#         # }
#         # filter_overrides = {
#         #     TagField: {  # TODO you'll need to look up the exact model field
#         #         'filter_class': django_filters.CharFilter,
#         #         'extra': lambda f: {
#         #             'lookup_expr': 'name__icontains',  # here we're saying to look through the icontains prop on name
#         #         },
#         #     },
#         #
#         # }

class ImgFilter(FilterSet):
    class Meta:
        model = Img  # 模型名

        fields = {
            'year': ['contains'],
            'month': ['gte', 'lte'],  # 判断搜索
            'day': ['gte', 'lte'],  # 判断搜索
            'filename': ['icontains']  # 模糊搜索
        }

        # fields = ['year', 'filename']  # 测试失败
        # filter_overrides = {
        #     models.IntegerField: {
        #         'filter_class': django_filters.NumberFilter,
        #         'extra': lambda f: {
        #             'lookup_expr': ['gte', 'lte'],
        #         },
        #     },
        #     models.CharField: {
        #         'filter_class': django_filters.CharFilter,
        #         'extra': lambda f: {
        #             'lookup_expr': 'icontains',
        #         },
        #     },
        #
        # }
