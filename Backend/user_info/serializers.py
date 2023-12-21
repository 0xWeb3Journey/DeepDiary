from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from library.serializers_out import FaceBriefSerializer
from tags.serializers import TagSerializerField
from user_info.models import Profile, Company, ROLES_OPTION, Demand, Resource, Experience, RELATION_OPTION, Image
from utilities.serializers import DisplayChoiceField


class UserRegisterSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='profile-detail', lookup_field='username')
    url = serializers.HyperlinkedIdentityField(view_name='profile-detail')

    class Meta:
        model = Profile
        fields = [
            'url',
            'id',
            'username',
            'password',
            'is_superuser'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'read_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    """于文章列表中引用的嵌套序列化器"""

    class Meta:
        model = Profile
        fields = [
            'id',
            'username',
            # 'last_login',
            # 'date_joined'
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    """于文章列表中引用的嵌套序列化器"""
    # 本级属性
    # profile_url = serializers.HyperlinkedIdentityField(view_name='profile-detail', lookup_field='username')
    profile_url = serializers.HyperlinkedIdentityField(view_name='profile-detail')
    # read_only=True, 允许表单roles为空
    roles = DisplayChoiceField(choices=ROLES_OPTION, read_only=True)  # 获取choice 属性值方式一：指定复写后的choice类,
    relation = TagSerializerField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'password', 'relation', 'tel', 'avatar', 'introduction', 'roles', 'profile_url',
                  'resources', 'demands']  #
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # user = Profile.objects.create_user(**validated_data)
        new_psw = make_password(validated_data["password"])
        print(f'validated_data is {validated_data}, password is {new_psw}')
        user = super(UserDetailSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])  # 用哈希算法对密码进行加密
        print(user.password)
        user.save()
        return user

    def update(self, instance, validated_data):
        print('this is UserRegisterSerializer_update')
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

    def to_representation(self, value):
        rst = {}
        # 调用父类获取当前序列化数据，value代表每个对象实例ob
        data = super().to_representation(value)
        # 对序列化数据做修改，添加新的数据
        rst['data'] = data
        rst['code'] = 200
        rst['msg'] = 'user profile'
        return rst


class ImageSerializer(serializers.ModelSerializer):
    thumb = serializers.ImageField(read_only=True)
    class Meta:
        model = Image
        fields = ['id', 'src', 'thumb']

    # def to_representation(self, instance):
    #     rst = []
    #     # 调用父类获取当前序列化数据，value代表每个对象实例ob
    #     data = super().to_representation(instance)
    #     if data is None:
    #         rst.append({
    #             # 其中id设置成4位的随机数
    #             'id': 1000,
    #             'src': 'https://deep-diary.oss-accelerate.aliyuncs.com/media/lg_logo.png',
    #             'thumb': 'https://deep-diary.oss-accelerate.aliyuncs.com/media/lg_logo.png',
    #         })
    #     return rst


class DemandSerializer(serializers.ModelSerializer):
    # 本级属性
    # demand_url = serializers.HyperlinkedIdentityField(view_name='demand-detail')
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Demand
        fields = ['id', 'name', 'desc', 'images']
        # fields = '__all__'
        # exclude = ['created_at', 'updated_at']


class ResourceSerializer(serializers.ModelSerializer):
    # 本级属性
    # resource_url = serializers.HyperlinkedIdentityField(view_name='resource-detail')
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Resource
        fields = ['id', 'name', 'desc', 'images']
        # fields = '__all__'
        # exclude = ['created_at', 'updated_at']


class ExperienceSerializer(serializers.ModelSerializer):
    # 本级属性
    # experience_url = serializers.HyperlinkedIdentityField(view_name='experience-detail')
    company = serializers.CharField(source="company.name", read_only=True)
    company_PyInitial = serializers.CharField(source="company.name_PyInitial", read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    class Meta:
        model = Experience
        # fields = ['name', 'addr', 'desc', 'company_url']
        # fields = '__all__'
        exclude = ['profile', 'created_at', 'updated_at']


class CompanySerializer(serializers.ModelSerializer):
    """于文章列表中引用的嵌套序列化器"""
    # 本级属性
    company_url = serializers.HyperlinkedIdentityField(view_name='company-detail')

    class Meta:
        model = Company
        # fields = ['name', 'addr', 'desc', 'company_url']
        # fields = '__all__'
        exclude = ['created_at', 'updated_at']


class ProfileSerializer(serializers.ModelSerializer):
    """于文章列表中引用的嵌套序列化器"""
    # 本级属性
    profile_url = serializers.HyperlinkedIdentityField(view_name='profile-detail')
    roles = DisplayChoiceField(choices=ROLES_OPTION, read_only=True)  # 获取choice 属性值方式一：指定复写后的choice类
    # faces = FaceBriefSerializer(many=True, read_only=True)
    demands = DemandSerializer(many=True, read_only=True)
    resources = ResourceSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True)  # , read_only=True
    relation = serializers.SerializerMethodField()

    def get_relation(self, instance):

        # 获取当前登录用户
        current_user = self.context['request'].user
        # print(f'current_user is {current_user}')
        # 在representation中添加当前登录用户的信息
        if isinstance(current_user, AnonymousUser):
            # current_user is an anonymous user
            # Perform actions specific to anonymous users
            return None
        else:
            # current_user is not an anonymous user
            # Perform actions for authenticated users

            recontact = instance.re_from_relations.filter(re_to=current_user).first()  # 有多条数据
            if recontact:
                return RELATION_OPTION[recontact.relation][1]
            return None

    class Meta:
        model = Profile
        fields = ['id', 'name', 'relation', 'avatar', 'introduction', 'roles', 'profile_url', 'demands', 'resources',
                  'experiences']
        # fields = '__all__'

    def to_representation(self, value):
        rst = {}
        # 调用父类获取当前序列化数据，value代表每个对象实例ob
        data = super().to_representation(value)
        # 对序列化数据做修改，添加新的数据
        rst['data'] = data
        rst['code'] = 200
        rst['msg'] = 'profile detail info'
        return rst
