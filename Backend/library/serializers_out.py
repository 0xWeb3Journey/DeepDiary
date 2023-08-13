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
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')
    thumb = serializers.ImageField(source="avatar_thumb", read_only=True)
    src = serializers.ImageField(source="avatar", read_only=True)
    # # imgs = ImgSerializer(many=True, read_only=True)  # this imgs must be the same as the related name in the model
    # value = serializers.IntegerField()
    value = serializers.SerializerMethodField()  # method 2: through method
    children = RecursiveField(many=True, required=False)


    @extend_schema_field(int)  # 提供额外的类型信息
    def get_value(self, ins):
        value = ins.imgs.count()  # return the img counts
        return value

    class Meta:
        model = Category
        fields = ['id', 'name', 'url', 'children', 'src', 'thumb', 'value']


class ImgGraphSerializer(serializers.ModelSerializer):
    tags = TagSerializerField(read_only=True)
    image = serializers.ImageField(source="src", read_only=True)
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
