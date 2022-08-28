# face/view.py
import os

from django.shortcuts import render
import numpy as np
# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from shutil import move

from deep_diary.settings import FACE_ROOT, FACE_INFO_ROOT
from face.models import Face, FaceAlbum
from face.pagination import FacePageNumberPagination
from face.serializers import FaceSerializer, FaceDetailSerializer, FaceAlbumSerializer, FaceAlbumDetailSerializer


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
        if not change_face_name(fc, serializer):  # 如果执行了改名，则返回真，人脸改名后，确认状态自动为True
            change_confirm_state(fc, serializer)  # 人名已经是识别出来的名字，进行确认后，同样要计算人脸特征

    def get_serializer_class(self):
        if self.action == 'list':
            return FaceSerializer
        else:
            return FaceDetailSerializer


class FaceAlbumViewSet(viewsets.ModelViewSet):
    queryset = FaceAlbum.objects.all()

    # serializer_class = FaceAlbumSerializer
    # permission_classes = (AllowAny,)
    pagination_class = FacePageNumberPagination

    def perform_update(self, serializer):  # 应该在调用的模型中添加
        print(f'当前访问人脸相册的用户是 =  {self.request.user}')

        album = self.get_object()
        change_album_name(album, serializer)  # 相册改名后，对应的人脸都需要改名，或者后续直接用相册名字

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


def change_confirm_state(fc, serializer):  # fc 更新前的实例对象，serializer： 更新后并经过校验的序列化器
    data = serializer.validated_data
    # print(f'INFO serializer.validated_data{data}')
    old_confirm = fc.is_confirmed
    new_confirm = data['is_confirmed']
    if old_confirm != new_confirm:
        # 3. 人脸相册数据库更新
        album = update_album_database(fc.name)

        # 4. 保存相关人脸信息到数据库
        fc_obj = serializer.save()  # 执行 is_confirmed = True 到数据库

        # 5. 更新并保存该人脸所有特征和中心特征到文件系统，并返回结果
        fts, cft = save_people_feats(fc.name)

        # 6. 更新并保存所有人脸姓名和中心特征到文件系统，并返回结果
        names, all_fts = save_all_feats()

        # 7. 根据计算好的中心向量，更新该人脸所有的相似度
        update_face_sim(fc.name, cft)

        return True
    return False


def change_face_name(fc, serializer):  # fc 更新前的实例对象，serializer： 更新后并经过校验的序列化器
    # data = self.request.data.copy()
    data = serializer.validated_data
    # print(f'INFO serializer.validated_data{data}')
    old_name = fc.name
    new_name = data['name']
    print(f'人脸更新：新的人脸是 {old_name} --> {new_name}')
    if old_name != new_name:
        # 1. 更新数据库路径信息
        new_img_path, new_info_path = update_face_path(fc, old_name, new_name)

        # 2. 移动相关文件, TODO 特性向量还是没有移动，后续需要优化：移出去，移回来后，就多了一个特征向量
        move_face_file(fc.src.path, old_name, new_name)  # 移动文件
        move_face_file(fc.face_info.path, old_name, new_name)
        # print(f'INFO new_img_path = {new_img_path}，new_info_path = {new_info_path}')

        # 3. 人脸相册数据库更新
        album = update_album_database(new_name)

        # 4. 保存相关人脸信息到数据库
        face = serializer.save(src=new_img_path, face_info=new_info_path,
                               face_album_id=album.id, is_confirmed=True)  # 序列化器貌似无法直接更新外键

        # 5. 更新并保存该人脸所有特征和中心特征到文件系统，并返回结果
        fts, cft = save_people_feats(new_name)

        # 6. 更新并保存所有人脸姓名和中心特征到文件系统，并返回结果
        names, all_fts = save_all_feats()

        # 7. 根据计算好的中心向量，更新所有人脸的相似度
        update_face_sim(new_name, cft)
        return True

    return False


def change_album_name(album, serializer):
    data = serializer.validated_data

    old_name = album.name
    new_name = data['name']
    if old_name != new_name:
        print(f'人脸相册名字更新：新的名字是 {old_name} --> {new_name}')

        # 1. 更新相册中的人脸及中心特征
        new_face_feat = album.face_feat.name.replace(old_name, new_name)
        serializer.save(face_feat=new_face_feat)  # 更新相册中的名字

        # 2. 更新人脸数据库中的名字，信息路径
        querys = Face.objects.filter(name=old_name)  # 获取并更新人脸照片中的名字
        for query in querys:
            query.name = new_name
            query.src, query.face_info = update_face_path(query, old_name, new_name)
        # print(querys)
        Face.objects.bulk_update(querys, ['name', 'src', 'face_info'])  # 这里的更新，不经过Face 视图级中的perform update

        # 3. 更改文件系统中文件夹名称: 重命名人脸目录，b. 重命名人脸信息目录
        fc_fold = os.path.join(FACE_ROOT, old_name)
        fc_info_fold = os.path.join(FACE_INFO_ROOT, old_name)
        new_fc_fold = os.path.join(FACE_ROOT, new_name)
        new_fc_info_fold = os.path.join(FACE_INFO_ROOT, new_name)
        if not os.path.exists(new_fc_fold):  # 如果文件夹不存在
            os.rename(fc_fold, new_fc_fold)
        else:  # 如果文件夹已存在
            pass  # 移动所有文件到已存在的目录
        if not os.path.exists(new_fc_info_fold):  # 如果文件夹不存在
            os.rename(fc_info_fold, new_fc_info_fold)
        else:  # 如果文件夹已存在
            pass  # 移动所有文件到已存在的目录, 合并人脸特征。

        # 4. 更新并保存该人脸所有特征和中心特征到文件系统，并返回结果
        fts, cft = save_people_feats(new_name)

        # 5. 更新并保存所有人脸姓名和中心特征到文件系统，并返回结果
        names, all_fts = save_all_feats()


def update_face_path(query, old_name, new_name):
    new_src = ''
    new_face_info = ''
    if query.src.name:
        new_src = query.src.name.replace(old_name, new_name)  # 更新数据库内容
    if query.face_info.name:
        new_face_info = query.face_info.name.replace(old_name, new_name)
    return new_src, new_face_info


def move_face_file(old_path, old_name, new_name):
    # 移动文件存储位置
    if not os.path.exists(old_path):  # 源路径不存在
        return

    new_img_path = old_path.replace(old_name, new_name)

    if not os.path.exists(os.path.dirname(new_img_path)):
        os.makedirs(os.path.dirname(new_img_path), exist_ok=True)
    move(old_path, new_img_path)

    print(f'移动文件并重命名，原文件 {old_path},目标目录{new_img_path}')


def update_album_database(face_name, face_info, face_src):
    """
    输入：
        更新后的名字
    输出：
        album: 更新后的相册对象
    """

    # face_feat = os.path.join('face_info', new_name, 'center_feats.txt')  #
    album = FaceAlbum.objects.filter(name=face_name)
    # TODO 对老相册如何处理？中心特征向量依然存在的
    if album.exists():
        album = album.first()  # 不加get-->AttributeError: 'TreeQuerySet' object has no attribute 'id'
        album.name = face_name
        album.face_feat = face_info
        album.avatar = face_src
        album.is_has_feat = True
        album.save()
        print(f"INFO the face album already exist, name is  {album.name}")
    else:
        # album = FaceAlbum.objects.create(name=face_name)
        album = FaceAlbum.objects.create(name=face_name, face_feat=face_info, avatar=face_src, is_has_feat=True)
        print(f"INFO the face album not exist, creating now, the new album id is {album.id}")

    return album


def save_people_feats(name):  # 保存所有人脸的中心特征

    fts_pth = os.path.join(FACE_INFO_ROOT, name, 'all_feats.txt')
    cft_pth = os.path.join(FACE_INFO_ROOT, name, 'center_feat.txt')

    fts, cft = get_people_fts(name)

    np.savetxt(fts_pth, fts, delimiter=',', fmt='%.4f')  # 保存所有人脸特征
    np.savetxt(cft_pth, cft, delimiter=',', fmt='%s')  # 保存所有人对应人名

    return fts, cft


def get_people_fts(name):
    """
    输入：
        name:一个人人脸的姓名
    输出：
        fts: 所有人脸特征
        cft: 该人的人脸特征中心
    """
    # print(f'INFO start getting {name} feats...')
    faces = Face.objects.filter(det_method=True, is_confirmed=True, name=name)
    # print(faces)
    fts = np.array([])
    cft = np.array([])
    for i in range(len(faces)):
        fc_info = np.load(faces[i].face_info.path, allow_pickle=True)
        ft = fc_info.item().normed_embedding.reshape(1, -1)
        # print(ft.shape)
        fts = ft if i == 0 else np.concatenate((fts, ft), axis=0)

    if fts.ndim == 2:  # fts 有数据，ndim是2
        cft = fts.mean(axis=0).reshape(1, -1)  # 将数组a转化为行向量
    return fts, cft
    # else:  # fts 无数据，ndim是1
    #     return None, None


def save_all_feats():  # 保存所有人脸的中心特征

    combined_fts_pth = os.path.join(FACE_INFO_ROOT, 'combined_feats.txt')
    names_pth = os.path.join(FACE_INFO_ROOT, 'names.txt')

    names, all_fts = get_all_fts()

    np.savetxt(combined_fts_pth, all_fts, delimiter=',', fmt='%.4f')  # 保存所有人脸特征
    np.savetxt(names_pth, names, delimiter=',', fmt='%s')  # 保存所有人对应人名

    return names, all_fts


def get_all_fts():  # 获取所有人脸的中心特征
    """
    输入：
        None
    输出：
        names: 所有已识别的人脸名字
        all_fts: 所有人脸特征中心的集合
    """
    names = []  # 保存所有人脸名字
    all_fts = np.array([])

    albums = FaceAlbum.objects.filter(is_has_feat=True)

    for album in albums:  # 直接从人脸相册中获取
        names = np.append(names, album.name)
        fc_info = np.load(album.face_feat.path, allow_pickle=True)
        ft = fc_info.item().normed_embedding.reshape(1, -1)
        # print(ft)
        # all_fts = np.concatenate(all_fts, ft)
        all_fts = ft if all_fts.ndim == 1 else np.concatenate((all_fts, ft), axis=0)  # all_fts != 2 表示all_fts还没有数据

    # for i in range(len(albums)):  # 重新计算不同人脸的中心向量
    #     # names.append(album.name)
    #
    #     fts, cft = get_people_fts(albums[i].name)
    #     if fts.ndim == 2:  # fts 有数据，ndim是2:
    #         # print(f'INFO face_{i}:fts shape is {fts.shape}, cft shape is {cft.shape}')
    #         # print(f'INFO face_{i}:fts ndim is {fts.ndim}, cft ndim is {cft.ndim}')
    #         # print(f'INFO face_{i}:all_fts ndim is {all_fts.ndim}')
    #         names = np.append(names, albums[i].name)
    #         # all_fts = cft if i == 0 else np.concatenate((all_fts, cft), axis=0)
    #         all_fts = cft if all_fts.ndim == 1 else np.concatenate((all_fts, cft), axis=0)  # all_fts != 2 表示all_fts还没有数据
    return names, all_fts


def update_face_sim(name, cft):
    """
    输入：
        该人脸的中心特征
    输出：
        album: 更新后的相册对象
    """

    faces = Face.objects.filter(det_method=True, is_confirmed=True, name=name)
    # print(f'INFO: total found  {len(faces)} faces instance, based on the name of {name}')

    for i in range(len(faces)):
        fc_info = np.load(faces[i].face_info.path, allow_pickle=True)
        ft = fc_info.item().normed_embedding.reshape(1, -1)
        faces[i].face_score = np.matmul(ft, cft.T)
        # print(f'INFO faces[i].face_score {faces[i].face_score}')
    Face.objects.bulk_update(faces, ['face_score'])  # 这里的更新，不经过Face 视图级中的perform update
    # return fts, cft


def get_face_name(ft, based='database'):
    """
    输入：
        None
    输出：
        name: 估算出来的人脸姓名
        sim: 是该人的相似度
    """
    names = []
    all_fts = []
    if based == 'os':
        combined_fts_pth = os.path.join(FACE_INFO_ROOT, 'combined_feats.txt')
        names_pth = os.path.join(FACE_INFO_ROOT, 'names.txt')
        if os.path.exists(combined_fts_pth):
            all_fts = np.loadtxt(combined_fts_pth, delimiter=',', dtype=float, skiprows=0, comments='#')  # 加载现有的所有人脸特征
            if all_fts.ndim == 1:  # 如果是一维数据，则转换成行向量
                all_fts = all_fts.reshape(1, -1)
        if os.path.exists(names_pth):
            names = np.loadtxt(names_pth, delimiter=',', dtype=str, skiprows=0, comments='#')  # 加载现有的所有人名

    if based == 'database':
        names, all_fts = get_all_fts()  # 得到所有的人名和中心向量

    # print(f'INFO names is {names}')
    # print(f'INFO all_fts.shape is {all_fts.shape}')

    sims = np.matmul(all_fts, ft.T)
    # print(f'INFO sims is {sims}')
    idx = sims.argmax()
    # print(f'INFO idx is {idx}')
    name = names[idx]
    sim = sims[idx]

    if sim > 0.3:  # 相似度比较高
        print('--------------------------------------------------------------------')
        print(f'\033[1;32m INFO: estimated name is {name}, p is {sim} \033[0m')  # \033[0m 是系统默认颜色
        print('--------------------------------------------------------------------')
    else:
        print(f'could not found the similar face from the database')
        name = 'unknown'
    return name, sim



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