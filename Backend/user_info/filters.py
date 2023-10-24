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

from user_info.models import Profile, ReContact, string_to_int_mapping

# only for text search
search_fields_profile = {
    'id': ['exact'],  #
    'name': ['exact', 'icontains'],
    'full_pinyin': ['exact', 'icontains'],
    'lazy_pinyin': ['exact', 'icontains'],
    'companies__name': ['exact', 'icontains'],
    'companies__name_PyFull': ['exact', 'icontains'],
    'companies__name_PyInitial': ['exact', 'icontains'],

}


class ProfileFilter(FilterSet):
    relation = django_filters.CharFilter('profile', method='relation_filter')
    confirmed = django_filters.CharFilter('name', method='confirmed_filter')

    class Meta:
        model = Profile  # 模型名

        fields = {
            'name': ['exact', 'icontains'],
            'id': ['exact', 'isnull','gt','lt'],
            'face_imgs__profiles': ['exact', 'isnull'],
            'companies': ['exact', 'isnull'],
            'companies__name': ['exact', 'icontains'],
            'faces': ['isnull'],
            're_from_relations': ['exact', 'isnull'],
            're_to_relations': ['exact', 'isnull'],
            're_from_relations__re_from': ['exact', 'isnull'],
            're_from_relations__re_to': ['exact', 'isnull'],
            're_from_relations__relation': ['exact', 'isnull'],

            're_to_relations__re_from': ['exact', 'isnull'],
            're_to_relations__re_to': ['exact', 'isnull'],
            're_to_relations__relation': ['exact', 'isnull'],

            'asserts__img_cnt': ['exact', 'isnull', 'gt', 'lt'],
            'asserts__face_cnt': ['exact', 'isnull', 'gt', 'lt'],
            'asserts__friend_cnt': ['exact', 'isnull', 'gt', 'lt'],

        }

    def relation_filter(self, qs, name, value):
        relation = string_to_int_mapping.get(value, None)
        user = self.request.user

        if not relation:
            profile_ids = ReContact.objects.exclude(re_to=user.id).values_list('re_from', flat=True)
        else:
            profile_ids = ReContact.objects.filter(relation=relation, re_to=user.id).values_list('re_from', flat=True)

        # print('relation_filter: ', name, value, relation, user.id)
        # print(profile_ids)
        qs = qs.filter(id__in=profile_ids)

        return qs

    def confirmed_filter(self, qs, name, value):
        # print('confirmed_filter: ', name, value)
        # 去掉那些name以'unknown'开头的记录
        if value == '1':
            # print('confirmed_filter: exclude the unknown profile', name, value)
            qs = qs.exclude(name__startswith='unknown')
        elif value == '0':
            # print('confirmed_filter: include the unknown profile', name, value)
            qs = qs.filter(name__startswith='unknown')
        else:
            qs = qs

        return qs


class RelationFilter(FilterSet):
    class Meta:
        model = ReContact  # 模型名

        fields = {
            'relation': ['exact'],
            'nickname': ['exact', 'icontains'],
            'PyInitial': ['exact', 'icontains'],
            'quanpin': ['exact', 'icontains'],
            'conRemark': ['exact', 'icontains'],
            'conRemarkPYFull': ['exact', 'icontains'],
            'conRemarkPYShort': ['exact', 'icontains'],
            'desc': ['exact', 'icontains'],
            're_from': ['exact'],
            're_to': ['exact'],

        }
