from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from user_info.models import Profile, ReContact, RELATION_OPTION
from utils.serializers import DisplayChoiceField


class ProfileBriefSerializer(serializers.ModelSerializer):
    """于文章列表中引用的嵌套序列化器"""
    # 本级属性
    profile_url = serializers.HyperlinkedIdentityField(view_name='profile-detail')
    thumb = serializers.ImageField(source="avatar", read_only=True)
    # 这个relation，来自与ReContact模型，Profile是外键，所以是反向查询，如下这行代码需要修改下

    # 这里有效，是因为在视图中使用了queryset = Profile.objects.all().annotate(value=Count('faces')).order_by('-value')
    # value = serializers.IntegerField()

    value = serializers.SerializerMethodField()  # method 2: through method

    def get_value(self, ins):
        value = ins.faces.count()  # return the img counts
        return value

    # relation = serializers.IntegerField(source='re_from_relations.relation', read_only=True)
    # relation = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'name', 'avatar', 'thumb', 'profile_url', 'value']


class ProfileGraphSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="avatar", read_only=True)
    label = serializers.CharField(source="name", read_only=True)
    # desc = serializers.CharField(source="caption", read_only=True)
    value = serializers.SerializerMethodField()  # method 2: through method
    categories = serializers.SerializerMethodField()  # method 2: through method

    def get_value(self, ins):
        value = 40  # return the img counts
        return value

    def get_categories(self, ins):
        value = ['person']
        return value

    class Meta:
        model = Profile
        fields = ['id', 'image', 'label', 'value', 'categories']


class RelationChoiceField(serializers.ChoiceField):  # 获取choice 属性值方式一, 重写Field 类

    def to_representation(self, obj):
        """返回选项的值"""
        return self._choices[obj]


class ReContactGraphSerializer(serializers.ModelSerializer):
    # 本级属性
    # recontact_url = serializers.HyperlinkedIdentityField(view_name='recontact-detail')
    # 需要做一个转换：
    # 把re_from换成from
    # 把re_to换成to
    # 把relation换成label, 同时，默认返回的是数字，需要基于RELATION_CHOICES做一个转换
    # 显示节点名称
    # re_from = serializers.CharField(source='re_from.name')
    # to = serializers.CharField(source='re_to.name')
    # 显示节点ID

    label = RelationChoiceField(choices=RELATION_OPTION, source='relation')  # 获取choice 属性值方式一：指定复写后的choice类

    class Meta:
        model = ReContact
        fields = ['re_from', 're_to', 'label']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['from'] = representation.pop('re_from')
        representation['to'] = representation.pop('re_to')
        return representation
