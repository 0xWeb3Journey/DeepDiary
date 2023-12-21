from rest_framework import serializers

from ad.models import Ad


class AdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = ['title', 'url']
