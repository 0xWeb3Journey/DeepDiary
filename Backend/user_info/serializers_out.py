from rest_framework import serializers

from user_info.models import Profile


class ProfileBriefSerializer(serializers.ModelSerializer):
    """于文章列表中引用的嵌套序列化器"""
    # 本级属性
    profile_url = serializers.HyperlinkedIdentityField(view_name='profile-detail')

    class Meta:
        model = Profile
        fields = ['id', 'name', 'avatar', 'profile_url']
        # fields = '__all__'