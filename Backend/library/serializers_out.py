from django.db.models import Count
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from library.models import Face, ColorBackground, ColorForeground, ColorItem, ColorImg, Color, Category
from utils.serializers import RecursiveField


class FaceBriefSerializer(serializers.ModelSerializer):
    face_url = serializers.HyperlinkedIdentityField(view_name='face-detail')

    class Meta:
        model = Face
        fields = ['id', 'face_url', 'src']


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
    # src = serializers.ImageField(source="avatar", read_only=True)
    # # imgs = ImgSerializer(many=True, read_only=True)  # this imgs must be the same as the related name in the model
    value = serializers.SerializerMethodField()  # method 2: through method
    children = RecursiveField(many=True, required=False)

    @extend_schema_field(int)  # 提供额外的类型信息
    def get_value(self, ins):
        value = ins.imgs.count()  # return the img counts
        return value

    class Meta:
        model = Category
        fields = ['id', 'name', 'value', 'url', 'children']
