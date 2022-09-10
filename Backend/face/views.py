# face/view.py

# Create your views here.
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action

from face.models import Face, FaceAlbum
from face.pagination import FacePageNumberPagination
from face.serializers import FaceSerializer, FaceDetailSerializer, FaceAlbumSerializer, FaceAlbumDetailSerializer
from face.task import change_album_name, change_face_name, change_confirm_state
from rest_framework.response import Response


class FaceViewSet(viewsets.ModelViewSet):
    queryset = Face.objects.all()
    # serializer_class = FaceSerializer
    # permission_classes = (AllowAny,)
    pagination_class = FacePageNumberPagination  # 增加了这句代码，就无法显示filter,不过效果还是有的

    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]  # 模糊过滤，注意的是，这里的url参数名变成了?search=搜索内容
    filterset_fields = ['face_album__id', 'img__id', 'name']  # 外键需要增加2个下划线
    # filterset_fields = ['img', 'name', 'is_confirmed', 'face_score']
    search_fields = ['face_album__id', 'img__id', 'name']
    ordering_fields = ['name']  # 这里的字段，需要总上面定义字段中选择

    # def perform_create(self, serializer):
    # print(f"INFO:{self.request.user}")
    # serializer.save(user=self.request.user)
    #     pass
    #
    def perform_update(self, serializer):  # 应该在调用的模型中添加
        # print(f'人脸更新：validated_data =  {serializer.validated_data}')
        # print(f'人脸更新：validated_data =  {self.request.data}')
        print(f'当前访问人脸的用户是 =  {self.request.user}')

        fc = self.get_object()
        change_face_name(fc, serializer)  # 如果执行了改名，则返回真，人脸改名后，确认状态自动为True
        # if not change_face_name(fc, serializer):  # 如果执行了改名，则返回真，人脸改名后，确认状态自动为True
        #     change_confirm_state(fc, serializer)  # 人名已经是识别出来的名字，进行确认后，同样要计算人脸特征

    def get_serializer_class(self):
        if self.action == 'list':
            return FaceSerializer
        else:
            return FaceDetailSerializer


class FaceAlbumViewSet(viewsets.ModelViewSet):
    queryset = FaceAlbum.objects.annotate(item_cnt=Count('faces')).order_by('-item_cnt')

    # serializer_class = FaceAlbumSerializer
    # permission_classes = (AllowAny,)
    pagination_class = FacePageNumberPagination

    def perform_update(self, serializer):  # 应该在调用的模型中添加
        print(f'当前访问人脸相册的用户是 =  {self.request.user}')

        album = self.get_object()
        # change_album_name.delay(album, serializer)  # 相册改名后，对应的人脸都需要改名，或者后续直接用相册名字
        old_name, new_name = change_album_name(album, serializer)  # 相册改名后，对应的人脸都需要改名，或者后续直接用相册名字

        print(serializer.validated_data)


    def get_serializer_class(self):
        if self.action == 'list':
            return FaceAlbumSerializer
        else:
            return FaceAlbumDetailSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]  # 模糊过滤，注意的是，这里的url参数名变成了?search=搜索内容
    filterset_fields = ['name', 'level']
    search_fields = ['name', 'level']
    ordering_fields = ['name']  # 这里的字段，需要总上面定义字段中选择

    @action(detail=False, methods=['get'])  # 在详情中才能使用这个自定义动作
    def clear_face_album(self, request, pk=None):  # 当detail=True 的时候，需要指定第三个参数，如果未指定look_up, 默认值为pk，如果指定，该值为loop_up的值
        # album_face_item = self.get_object()  # 获取详情的实例对象
        album_face_set = self.queryset.filter(item_cnt=0).delete()  # 获取查询集，过滤出没有子集的对象，删除
        # print(f'INFO album_face: {type(album_face_set)}')
        print(f'INFO delete result: {album_face_set}')
        data = {
            "data": "demo",
            "code": 200,
            "msg": "success to clear the Face Album "
        }
        return Response(data)

#
# # 更新所有人脸中心特征
# # 1. 相册刚创建
# # 2. 中心人脸有更新
# def update_combined_feats(album):
#     combined_fts_pth = os.path.join(FACE_INFO_ROOT, 'combined_feats.txt')
#     center_ft = np.loadtxt(album.face_feat.path, delimiter=',', dtype=float, skiprows=0,
#                            comments='#').reshape(1, -1)
#
#     if os.path.exists(combined_fts_pth):
#         all_fts = np.loadtxt(combined_fts_pth, delimiter=',', dtype=float, skiprows=0, comments='#')  # 加载现有的所有人脸特征
#         if all_fts.ndim == 1:  # 如果是一维数据，则转换成行向量
#             all_fts = all_fts.reshape(1, -1)
#         all_fts = np.concatenate((all_fts, center_ft), axis=0)
#         print(f'INFO all_fts already existed, the shape is {all_fts.shape}')
#     else:
#         all_fts = center_ft
#         print(f'INFO combined_fts_pth do not existed, creating now...')
#
#     names_pth = os.path.join(FACE_INFO_ROOT, 'names.txt')
#     if os.path.exists(names_pth):
#         names = np.loadtxt(names_pth, delimiter=',', dtype=str, skiprows=0, comments='#')  # 加载现有的所有人脸特征
#     else:
#         names = []
#     names = np.append(names, album.name)
#     print(f'INFO names is {names}')
#
#     np.savetxt(combined_fts_pth, all_fts, delimiter=',', fmt='%.4f')  # 保存所有人脸特征
#     np.savetxt(names_pth, names, delimiter=',', fmt='%s')  # 保存所有人对应人名

#
# def save_calc_feats(face_info_path):
#     fc_info = np.load(face_info_path, allow_pickle=True)
#     ft = fc_info.item().normed_embedding.reshape(1, -1)
#
#     fold = os.path.dirname(face_info_path)  # 保存该人的所有人脸特征
#     all_fts_pth = os.path.join(fold, 'all_feats.txt')
#     center_fts_pth = os.path.join(fold, 'center_feats.txt')
#     if os.path.exists(all_fts_pth):
#         all_fts = np.loadtxt(all_fts_pth, delimiter=',', dtype=float, skiprows=0, comments='#')  # 加载现有的所有人脸特征
#         if all_fts.ndim == 1:  # 如果是一维数据，则转换成行向量
#             all_fts = all_fts.reshape(1, -1)
#         print(f'INFO all_fts shape is {all_fts.shape}, fc_info.normed_embedding shape is {ft.shape}')
#         new_all_fts = np.concatenate((all_fts, ft), axis=0)
#     else:
#         new_all_fts = ft
#     np.savetxt(all_fts_pth, new_all_fts, delimiter=',', fmt='%.4f')  # 保存该人的所有人脸特征
#
#     center_fts = new_all_fts.mean(axis=0).reshape(1, -1)  # 将数组a转化为行向量
#     np.savetxt(center_fts_pth, center_fts, delimiter=',', fmt='%.4f')  # 保存该人中心特征向量，后续改为网络模型计算中心特征
#
#     sim = np.matmul(ft, center_fts.T)
#     return center_fts_pth, sim
