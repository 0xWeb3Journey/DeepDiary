from django.db.models import Count
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from library.models import Face, ColorBackground, ColorForeground, ColorItem, ColorImg, Color, Category, Img
from tags.serializers import TagSerializerField
from utils.serializers import RecursiveField


class FaceBriefSerializer(serializers.ModelSerializer):
    face_url = serializers.HyperlinkedIdentityField(view_name='face-detail')
    img = serializers.ImageField(source="img.src", read_only=True)
    thumb = serializers.ImageField(source="src", read_only=True)
    # thumb_face = serializers.ImageField(source="src", read_only=True)
    # name = serializers.CharField(source="profile.name", read_only=True)
    name = serializers.SerializerMethodField()

    def get_name(self, instance):
        return instance.profile.name if instance.profile else "未命名"

    class Meta:
        model = Face
        fields = ['id', 'face_url', 'img', 'thumb', 'name']


class FaceGraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Face
        fields = ['img', 'profile']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['from'] = representation.pop('img')
        representation['to'] = representation.pop('profile')
        representation['label'] = 'include'
        return representation


class ColorItemBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorItem
        # fields = '__all__'
        fields = ['html_code', 'percent']


class ColorBackgroundBriefSerializer(ColorItemBriefSerializer):
    class Meta:
        model = ColorBackground
        fields = ['html_code', 'percent']


class ColorForegroundBriefSerializer(ColorItemBriefSerializer):
    class Meta:
        model = ColorForeground
        fields = ['html_code', 'percent']


class ColorImgBriefSerializer(ColorItemBriefSerializer):
    class Meta:
        model = ColorImg
        fields = ['html_code', 'percent']


class ColorBriefSerializer(serializers.ModelSerializer):
    background = ColorBackgroundBriefSerializer(many=True, read_only=True)
    foreground = ColorForegroundBriefSerializer(many=True, read_only=True)
    image = ColorImgBriefSerializer(many=True, read_only=True)

    class Meta:
        model = Color
        fields = '__all__'


class CategoryBriefSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='category-detail')
    thumb = serializers.ImageField(source="avatar_thumb", read_only=True)
    # src = serializers.ImageField(source="avatar", read_only=True)
    # # imgs = ImgSerializer(many=True, read_only=True)  # this imgs must be the same as the related name in the model
    # value = serializers.IntegerField()
    value = serializers.SerializerMethodField()  # method 2: through method
    # children = RecursiveField(many=True, required=False)

    @extend_schema_field(int)  # 提供额外的类型信息
    def get_value(self, ins):
        value = ins.imgs.count()  # return the img counts
        return value

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     # 检查 'children' 字段是否为空
    #     if not data['children']:
    #         # 如果为空，从字典中删除 'children' 字段
    #         del data['children']
    #     # print(data)
    #     # if instance.is_leaf_node():
    #     #     if not instance.children.exists():
    #     #         data.pop('children', None)  # Remove 'children' key if it's empty
    #     return data

    class Meta:
        model = Category
        fields = ['id', 'name', 'thumb', 'value']  #,'children'



class CategoryFilterListSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source="name", read_only=True)
    label = serializers.CharField(source="name", read_only=True)
    # count = serializers.SerializerMethodField()  # 增加这个语句，查询会特别慢
    # Category模型有个外键imgs的查询集合，期望将此序列化器的结果，限制在这个查询集中，而不是所有的Img模型实例
    # children = RecursiveField(many=True, required=False)

    children = serializers.SerializerMethodField()  # 使用 SerializerMethodField 处理 children

    def get_children(self, instance):
        # 获取子类别，仅包括在 imgs_queryset 内的子类别
        qs = self.context.get('imgs', None)
        if qs is None:
            children = instance.get_children()
        else:
            children = instance.get_children().filter(imgs__in=qs).distinct()

        # 递归处理子类别
        serializer = CategoryFilterListSerializer(children, many=True, context=self.context)
        return serializer.data

    def get_count(self, ins):
        value = ins.imgs.count()  # return the img counts
        # value = 10  # return the img counts
        # value = ins.img_count  # 我们假设 Category 模型具有一个名为 img_count 的字段，该字段存储了与该类别相关的图像数量
        return value

    class Meta:
        model = Category
        fields = ['value', 'label', 'children']  # ,'count'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 检查 'children' 字段是否为空
        if not data['children']:
            # 如果为空，从字典中删除 'children' 字段
            del data['children']
        # print(data)
        # if instance.is_leaf_node():
        #     if not instance.children.exists():
        #         data.pop('children', None)  # Remove 'children' key if it's empty
        return data


class ImgGraphSerializer(serializers.ModelSerializer):
    tags = TagSerializerField(read_only=True)
    image = serializers.ImageField(source="thumb", read_only=True)
    label = serializers.CharField(source="name", read_only=True)
    desc = serializers.CharField(source="caption", read_only=True)
    value = serializers.SerializerMethodField()  # method 2: through method
    categories = serializers.SerializerMethodField()  # method 2: through method

    def get_value(self, ins):
        value = 30  # return the img counts
        return value

    def get_categories(self, ins):
        value = ['image']
        return value

    class Meta:
        model = Img
        fields = ['id', 'image', 'tags', 'label', 'value', 'desc', 'categories', 'caption']
