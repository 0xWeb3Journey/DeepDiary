from django.shortcuts import render
from rest_framework import viewsets

from ad.models import Ad
from ad.serializers import AdSerializer
from utilities.pagination import GeneralPageNumberPagination


# Create your views here.

class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = GeneralPageNumberPagination  # could disp the filter button in the web
