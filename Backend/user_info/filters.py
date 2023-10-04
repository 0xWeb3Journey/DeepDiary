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

    class Meta:
        model = Profile  # 模型名

        fields = {
            'name': ['exact', 'icontains'],
            're_from_relations': ['exact', 'isnull'],
            're_to_relations': ['exact', 'isnull'],
            're_from_relations__re_from': ['exact', 'isnull'],
            're_from_relations__re_to': ['exact', 'isnull'],
            're_from_relations__relation': ['exact', 'isnull'],

            're_to_relations__re_from': ['exact', 'isnull'],
            're_to_relations__re_to': ['exact', 'isnull'],
            're_to_relations__relation': ['exact', 'isnull'],

        }

    def relation_filter(self, qs, name, value):
        relation = string_to_int_mapping.get(value, None)
        user = self.request.user

        if not relation:
            return qs
        print('relation_filter: ', name, value, relation, user.id)
        profile_ids = ReContact.objects.filter(relation=relation, re_to=user.id).values_list('re_from', flat=True)
        print(profile_ids)
        qs = qs.filter(id__in=profile_ids)

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
