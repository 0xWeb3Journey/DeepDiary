# user_info/views.py
import json

from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from user_info.models import Profile, Company
from user_info.serializers import UserRegisterSerializer, ProfileSerializer, CompanySerializer, \
    UserDetailSerializer
from user_info.serializers_out import ProfileBriefSerializer
# class UserRegisterViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = UserRegisterSerializer
#     lookup_field = 'username'  # 要和序列化器中对应起来
from utils.pagination import GeneralPageNumberPagination
from utils.permissions import get_user_info


class UserViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    # lookup_field = 'username'  # 要和序列化器中对应起来
    serializer_class = UserRegisterSerializer
    pagination_class = GeneralPageNumberPagination

    # permission_classes = [IsRegister]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserRegisterSerializer
        else:
            return UserDetailSerializer  # UserDetailSerializer

    @action(detail=False, methods=['get', 'post'])  # detail=False, 接口外面调用，如果是True，在详情中调用
    def info(self, request, username=None):

        # print(f'INFO self: {dir(self.request)}')  # 在这个类中定义函数，都可以通过self获取相关数据，
        # print(f'INFO request: {dir(request)}')  # 跟上面结果一致
        # print(f'INFO request.query_params: {request.query_params}')  # 头部参数信息
        # print(f'INFO request.auth: {request.auth}')  # 如果是用token 验证方式，这里对应的就是token值
        # print(f'INFO request.authenticators: {request.authenticators}')
        # print(f'INFO request.data: {request.data}')  # 请求body信息
        # print(f'INFO request.user: {request.user}')  # 如果是用token验证方式，通过这个就可以获取对应的用户名
        # user_obj = User.objects.filter(username=request.user).first()  # 通过Bearer Token 方式获取用户信息
        user_obj = get_user_info(request)

        if user_obj:
            print(f'INFO: success login: the user name is: {user_obj.username}')
            serializer = UserDetailSerializer(user_obj, many=False, context={'request': request})  # 这里不加context 就会报错
            # serializer = UserRegisterSerializer(queryset, many=False, context={'request': request})  # 这里不加context 就会报错
            rst_data = serializer.data['data']
            # # print(f'INFO rst_data: {rst_data}')
            # role = []
            # # print(rst_data['roles'])
            # role.append(rst_data['roles'])
            # # print(role)
            # rst_data['roles'] = role
            # # print(rst_data['roles'])
            # TODO need to debug later
            rst_data['roles'] = ['admin']
            data = {

                "data": rst_data,
                "code": 200,
                "message": "用户信息获取成功"
            }
        else:
            data = {

                "code": 400,
                "message": "the user is not existed"
            }
        # print(f'INFO: success to get the info:\n {json.dumps(data, indent=4)}')
        print(f'INFO: success to get the info:\n')
        return Response(data)

    @action(detail=False)  # 在列表中才能使用这个自定义动作
    def sorted(self, request):
        users = User.objects.all().order_by('-username')

        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])  # detail=False, 接口外面调用，如果是True，在详情中调用
    def logout(self, request, username=None):
        logout(request)
        data = {
            "code": 200,
            "msg": "success logout"
        }
        return Response(data)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().annotate(value=Count('faces')).order_by('-value')
    pagination_class = GeneralPageNumberPagination

    def perform_update(self, serializer):
        print('------------------Profile Perform_update------------------')
        face_id = self.request.data.get("id", None)
        print(f'人物更新：validated_data =  {serializer.validated_data}')
        print(f'人脸ID：face_id =  {face_id}')
        print(f'当前访问的用户是 =  {self.request.user}')
        instance = self.get_object()  # 获取详情的实例对象
        face_ins = instance.faces.filter(id=face_id).first()
        if face_ins:
            # instance.avatar = face_ins.src
            # instance.embedding = face_ins.embedding
            serializer.validated_data["avatar"] = face_ins.src
            serializer.validated_data["embedding"] = face_ins.embedding
        else:
            print("未找到匹配的face_ins")

        serializer.save()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProfileBriefSerializer
        else:
            return ProfileSerializer

    @action(detail=True, methods=['get'])  # 在详情中才能使用这个自定义动作
    def change_avatar(self, request, pk=None):  # 当detail=True 的时候，需要指定第三个参数，如果未指定look_up, 默认值为pk，如果指定，该值为loop_up的值
        print('------------------changeAvatar_process------------------')
        instance = self.get_object()  # 获取详情的实例对象
        # 从request中获取参数
        param = request.query_params
        print(f'INFO:-> param: {param}')

        face_id = param.get("face_id", None)
        print(f'INFO:-> face_id: {face_id}')
        face_ins = instance.faces.filter(id=face_id).first()
        instance.avatar = face_ins.src
        instance.embedding = face_ins.embedding
        instance.save()
        # instance.update(avatar=face_ins.src, embedding=face_ins.embedding)
        profile = ProfileSerializer(instance, many=False, context={'request': request})
        rst = {
            "data": profile.data,
            "code": 200,
            "msg": "success change avatar"
        }
        print('------------------changeAvatar_process finished------------------')
        return Response(rst)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
