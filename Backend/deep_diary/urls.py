"""deep_diary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from comment.views import CommentViewSet
from library.views import ImgViewSet, ImgCategoryViewSet, ImgMcsViewSet, CategoryViewSet, AddressViewSet, FaceViewSet
from project.views import ProjectViewSet, ProductViewSet, ToolingViewSet, OutsourcingViewSet, PurchaseViewSet, \
    DeliveryViewSet, ResumeViewSet, IssueViewSet
from tags.views import TagViewSet
from user_info.views import UserViewSet, CompanyViewSet, ProfileViewSet, ReContactViewSet, ExperienceViewSet
from utils.views import AdViewSet

router = DefaultRouter()

router.register(r'imgcategory', ImgCategoryViewSet)
router.register(r'img', ImgViewSet)
router.register(r'face', FaceViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'tag', TagViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'user', UserViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'recontact', ReContactViewSet)
router.register(r'company', CompanyViewSet)
router.register(r'project', ProjectViewSet)  # 新增
router.register(r'product', ProductViewSet)  # 新增
router.register(r'tooling', ToolingViewSet)  # 新增
router.register(r'outsourcing', OutsourcingViewSet)  # 新增
router.register(r'purchase', PurchaseViewSet)  # 新增
router.register(r'delivery', DeliveryViewSet)  # 新增
router.register(r'resume', ResumeViewSet)  # 新增
router.register(r'issue', IssueViewSet)  # 新增
router.register(r'mcs', ImgMcsViewSet)  # 新增
router.register(r'ad', AdViewSet)  # 新增
router.register(r'category', CategoryViewSet)  # 新增
router.register(r'address', AddressViewSet)  # 新增
router.register(r'experience', ExperienceViewSet)  # 新增

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path(r'ckeditor/', include('ckeditor_uploader.urls')),
    path(r'mdeditor/', include('mdeditor.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # there is no api for original design
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # path("__debug__/", include("debug_toolbar.urls")),  # django-debug-toolbar 调试接口

]

# 把媒体文件的路由注册了
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

  urlpatterns.insert(0, path("__debug__/", include("debug_toolbar.urls")))

