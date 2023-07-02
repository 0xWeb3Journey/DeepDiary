# library/serializers.py
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from library.models import Img, Category, ImgMcs, Color, ColorItem, ColorBackground, ColorForeground, ColorImg, \
    ImgCategory, Address, Evaluate, Date, Kps, FaceLandmarks2D, Face, FaceLandmarks3D, Stat
from library.serializers_out import FaceBriefSerializer, ColorBriefSerializer
# 自定义TagSerializerField，将多个tag用英文逗号隔开。
from tags.serializers import TagSerializerField
from user_info.serializers_out import ProfileBriefSerializer
from utils.serializers import RecursiveField


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['img', 'is_located', 'country', 'province', 'city', 'district', 'location']

    def to_representation(self, value):
        # 调用父类获取当前序列化数据，value代表每个对象实例ob
        data = super().to_representation(value)
        data['lnglat'] = [value.longitude, value.latitude]
        return data


class EvaluateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluate
        fields = '__all__'


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = '__all__'


class ImgCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="category", read_only=True)

    class Meta:
        model = ImgCategory
        # fields = '__all__'
        exclude = ['created_at']


class ColorItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorItem
        fields = '__all__'
        # fields = ['html_code', 'percent']


class ColorBackgroundSerializer(ColorItemSerializer):
    class Meta:
        model = ColorBackground
        fields = '__all__'


class ColorForegroundSerializer(ColorItemSerializer):
    class Meta:
        model = ColorForeground
        fields = '__all__'


class ColorImgSerializer(ColorItemSerializer):
    class Meta:
        model = ColorImg
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    background = ColorBackgroundSerializer(many=True, read_only=True)
    foreground = ColorForegroundSerializer(many=True, read_only=True)
    image = ColorImgSerializer(many=True, read_only=True)

    class Meta:
        model = Color
        fields = '__all__'


class McsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImgMcs
        fields = ['nft_url']

    # def to_representation(self, value):
    #     rst={}
    #     # 调用父类获取当前序列化数据，value代表每个对象实例ob
    #     data = super().to_representation(value)
    #     # 对序列化数据做修改，添加新的数据
    #     rst['data'] = data
    #     rst['code'] = 200
    #     rst['msg'] = 'mcs detail info'
    #     return rst


class McsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImgMcs
        fields = '__all__'


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = '__all__'


# --------------------------------------------------face serializer
class FaceLandmarks3DSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceLandmarks3D
        fields = '__all__'


class FaceLandmarks2DSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceLandmarks2D
        fields = '__all__'


class KpsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kps
        fields = '__all__'


class FaceSerializer(serializers.ModelSerializer):
    face_url = serializers.HyperlinkedIdentityField(view_name='face-detail')
    # img = serializers.HyperlinkedRelatedField(view_name='img-detail', read_only=True)  # 替换为与视图中指定的查询字段一致
    # profile_url = serializers.HyperlinkedIdentityField(view_name='profile-detail')  # 此行代码有问题，待解决

    def create(self, validated_data):
        landmarks3d_data = validated_data.pop('landmarks3d', [])
        landmarks2d_data = validated_data.pop('landmarks2d', [])
        kps_data = validated_data.pop('kps', [])

        face = Face.objects.create(**validated_data)

        for landmark3d_data in landmarks3d_data:
            FaceLandmarks3D.objects.create(face=face, **landmark3d_data)

        for landmark2d_data in landmarks2d_data:
            FaceLandmarks2D.objects.create(face=face, **landmark2d_data)

        for kp_data in kps_data:
            Kps.objects.create(face=face, **kp_data)

        return face

    class Meta:
        model = Face
        fields = '__all__'


class FaceDetailSerializer(serializers.ModelSerializer):
    landmarks3d = FaceLandmarks3DSerializer(many=True, read_only=True)
    landmarks2d = FaceLandmarks2DSerializer(many=True, read_only=True)
    kps = KpsSerializer(many=True, read_only=True)

    def create(self, validated_data):
        landmarks3d_data = validated_data.pop('landmarks3d', [])
        landmarks2d_data = validated_data.pop('landmarks2d', [])
        kps_data = validated_data.pop('kps', [])

        face = Face.objects.create(**validated_data)

        for landmark3d_data in landmarks3d_data:
            FaceLandmarks3D.objects.create(face=face, **landmark3d_data)

        for landmark2d_data in landmarks2d_data:
            FaceLandmarks2D.objects.create(face=face, **landmark2d_data)

        for kp_data in kps_data:
            Kps.objects.create(face=face, **kp_data)

        return face

    class Meta:
        model = Face
        fields = '__all__'
        # exclude = ['kps', 'landmarks2d', 'landmarks3d']


class ImgSerializer(serializers.ModelSerializer):
    # user = ProfileSerializer(read_only=True)  # 2. 使用嵌套序列化器
    user = serializers.CharField(source="user.username", read_only=True)  # 2. 使用source选项 直接指定外键模型下面的具体字段
    tags = TagSerializerField(read_only=True)
    thumb = serializers.ImageField(read_only=True)
    img_url = serializers.HyperlinkedIdentityField(view_name='img-detail')

    # mcs = McsSerializer(serializers.ModelSerializer, read_only=True)  # read_only=True, 如果不添加这个配置项目，则必须要mcs这个字段
    # categories = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Img
        fields = ['user', 'id', 'src', 'thumb', 'tags', 'img_url', 'name']  # 'faces', 'names','mcs', 'categories'

    def to_representation(self, value):
        rst = {}
        # 调用父类获取当前序列化数据，value代表每个对象实例ob
        data = super().to_representation(value)
        # 对序列化数据做修改，添加新的数据
        # rst['data'] = data
        # rst['code'] = 200
        # rst['msg'] = 'list info'
        # return rst
        # print(data['categories'])
        # print(f'value.wid: {value.wid}, value.height: {value.height}')
        data['size'] = '{:d}-{:d}'.format(value.wid, value.height)
        if hasattr(value, 'address'):
            data['lnglat'] = [value.address.longitude, value.address.latitude]
        # library.models.Img.address.RelatedObjectDoesNotExist: Img has no address
        return data


class ImgDetailSerializer(ImgSerializer):  # 直接继承ImgSerializer也是可以的

    # 父级属性
    issue_url = serializers.HyperlinkedIdentityField(view_name='issue-detail')
    issue = serializers.CharField(source="issue.desc", read_only=True)
    # 子级属性：一对多

    names = SerializerMethodField(label='names', read_only=True)  # 获取子集模型字段的方法二，对于不存在的字段，临时添加字段，需要结合get_字段名()这个函数
    profiles = ProfileBriefSerializer(many=True, read_only=True)  # 这里的名字，必须是Profile 定义Img 外键时候的'related_name'
    faces = FaceBriefSerializer(many=True, read_only=True)  # 这里的名字，必须是Face 定义Img 外键时候的'related_name'
    dates = DateSerializer(read_only=True)  # this name should be the same as model related name
    evaluates = EvaluateSerializer(read_only=True)  # this name should be the same as model related name
    address = AddressSerializer(read_only=True)  # this name should be the same as model related name
    stats = StatSerializer(read_only=True)  # this name should be the same as model related name
    mcs = McsSerializer(read_only=True)  # read_only=True, 如果不添加这个配置项目，则必须要mcs这个字段
    colors = ColorBriefSerializer(read_only=True)  # this name should be the same as model related name

    def get_names(self, obj):
        print('type(obj)')
        query_set = obj.faces.all()
        # print('getting the faces now....')
        return [obj.profile.name for obj in query_set if obj.profile]

    class Meta:
        model = Img
        fields = '__all__'

    def to_representation(self, value):
        rst = {}
        # 调用父类获取当前序列化数据，value代表每个对象实例ob
        data = super().to_representation(value)
        # 对序列化数据做修改，添加新的数据
        rst['data'] = data
        rst['code'] = 200
        rst['msg'] = 'img detail info'
        return rst


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')
    src = serializers.ImageField(source="avatar", read_only=True)
    # imgs = ImgSerializer(many=True, read_only=True)  # this imgs must be the same as the related name in the model
    value = serializers.SerializerMethodField()  # method 2: through method

    @extend_schema_field(int)  # 提供额外的类型信息
    def get_value(self, ins):
        value = ins.imgs.count()  # return the img counts
        return value

    class Meta:
        model = Category
        fields = ['id', 'name', 'value', 'url', 'level', 'src', 'description', 'parent', 'children', 'imgs']
        # fields = '__all__'
        # exclude = ['', '']

    # def to_representation(self, value):
    #     rst = {}
    #     # 调用父类获取当前序列化数据，value代表每个对象实例ob
    #     data = super().to_representation(value)
    #     # 对序列化数据做修改，添加新的数据
    #     rst['data'] = data
    #     rst['code'] = 200
    #     rst['msg'] = 'category detail info'
    #     return rst


class CategoryDetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')
    src = serializers.ImageField(source="avatar", read_only=True)
    img = ImgSerializer(many=True, read_only=True)  # this imgs must be the same as the related name in the model

    class Meta:
        model = Category
        # fields = '__all__'
        exclude = ['avatar']

    def to_representation(self, value):
        rst = {}
        # 调用父类获取当前序列化数据，value代表每个对象实例ob
        data = super().to_representation(value)
        # 对序列化数据做修改，添加新的数据
        rst['data'] = data
        rst['code'] = 200
        rst['msg'] = 'category detail info'
        return rst
