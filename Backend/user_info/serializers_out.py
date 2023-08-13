from rest_framework import serializers

from user_info.models import Profile


class ProfileBriefSerializer(serializers.ModelSerializer):
    """于文章列表中引用的嵌套序列化器"""
    # 本级属性
    profile_url = serializers.HyperlinkedIdentityField(view_name='profile-detail')
    thumb = serializers.ImageField(source="avatar", read_only=True)
    value = serializers.IntegerField()
    # value = serializers.SerializerMethodField()  # method 2: through method

    def get_value(self, ins):
        value = ins.faces.count()  # return the img counts
        return value

    class Meta:
        model = Profile
        fields = ['id', 'name', 'avatar', 'thumb', 'profile_url', 'value']
        # fields = '__all__'


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

