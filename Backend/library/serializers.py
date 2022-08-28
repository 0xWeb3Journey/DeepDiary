# library/serializers.py

from rest_framework import serializers

# from face.models import Face
# from face.serializers import FaceSerializer
from rest_framework.fields import SerializerMethodField

from face.serializers import FaceSerializer, facesField, FaceSimpleSerializer
from library.models import Img, ImgCategory, Mcs
# 自定义TagSerializerField，将多个tag用英文逗号隔开。
from tags.serializers import TagSerializerField


class McsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mcs
        fields = '__all__'


class ImgCategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='imgcategory-detail')

    class Meta:
        model = ImgCategory
        fields = '__all__'


class ImgSerializer(serializers.ModelSerializer):
    # user = ProfileSerializer(read_only=True)  # 2. 使用嵌套序列化器
    user = serializers.CharField(source="user.username", read_only=True)  # 2. 使用source选项 直接指定外键模型下面的具体字段
    tags = TagSerializerField(read_only=True)
    thumb = serializers.ImageField(read_only=True)
    img_url = serializers.HyperlinkedIdentityField(view_name='img-detail')
    mcs = McsSerializer(serializers.ModelSerializer, read_only=True)  # read_only=True, 如果不添加这个配置项目，则必须要mcs这个字段

    class Meta:
        model = Img
        fields = ['user', 'id', 'src', 'thumb', 'tags', 'img_url', 'filename', 'mcs'] # 'faces', 'names',

    def to_representation(self, value):
        rst={}
        # 调用父类获取当前序列化数据，value代表每个对象实例ob
        data = super().to_representation(value)
        # 对序列化数据做修改，添加新的数据
        # rst['data'] = data
        # rst['code'] = 200
        # rst['msg'] = 'list info'
        # return rst

        data['size'] = '{:d}-{:d}'.format(value.wid, value.height)
        return data


class ImgDetailSerializer(ImgSerializer):  # 直接继承ImgSerializer也是可以的

    # 父级属性
    issue_url = serializers.HyperlinkedIdentityField(view_name='issue-detail')
    issue = serializers.CharField(source="issue.desc", read_only=True)
    # 子级属性：一对多
    # face = FaceSerializer(many=True, read_only=True)  # 这里的名字，必须是Face 定义Img 外键时候的'related_name'
    # names = facesField(many=True, read_only=True)  # 获取子集模型字段的方法一，指定序列化器
    faces = FaceSimpleSerializer(many=True, read_only=True)

    names = SerializerMethodField(label='names', read_only=True)  # 获取子集模型字段的方法二，对于不存在的字段，临时添加字段，需要结合get_字段名()这个函数



    def get_names(self, obj):
        query_set = obj.faces.all()
        # print('getting the faces now....')
        return [obj.name for obj in query_set]

    class Meta:
        model = Img
        fields = '__all__'

    def to_representation(self, value):
        rst={}
        # 调用父类获取当前序列化数据，value代表每个对象实例ob
        data = super().to_representation(value)
        # 对序列化数据做修改，添加新的数据
        rst['data'] = data
        rst['code'] = 200
        rst['msg'] = 'img detail info'
        return rst






