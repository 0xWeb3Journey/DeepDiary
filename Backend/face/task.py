import os
import random
import string

import cv2 as cv
import numpy as np
# Create your models here.
from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver
from insightface.app import FaceAnalysis

# os.environ.setdefault('DJANGO_SETTING_MODULE', 'deep-diary.settings')
# django.setup()
from deep_diary.config import wallet_info
from face.models import Face
from face.serializers import McsSerializer, McsDetailSerializer
from face.views import get_face_name, update_album_database
from mycelery.main import app
import os
import random
import string

import cv2 as cv
import django
import numpy as np
from PIL import Image as Image_PIL
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from insightface.app import FaceAnalysis
from pyexiv2 import Image as Image_pyexiv2

# os.environ.setdefault('DJANGO_SETTING_MODULE', 'deep-diary.settings')
# django.setup()
from face.models import Face, FaceAlbum
from face.views import get_face_name, save_people_feats, save_all_feats, update_face_sim, update_album_database
from library.models import Img
from utils.mcs_storage import upload_file_pay, upload_file_pay_face


class FaceInfo:
    def __init__(self):
        self.det_score = 0.0
        self.age = 0
        self.gender = 0
        # ndarrary
        self.normed_embedding = 0
        self.bbox = 0
        self.kps = 0
        self.landmark_2d_106 = 0
        self.landmark_3d_68 = 0
        self.pose = 0


# 通过LightRoom人脸识别的方式，保存相关人脸信息
def save_LM_faces(img):
    print(f'INFO: save_LM_faces ... ')
    names, bboxs = get_LM_face_info(img)
    face = Face()
    for [name, bbox] in [names, bboxs]:
        face.name = name
        face.x = bbox[0]
        face.y = bbox[1]
        face.wid = bbox[2] - bbox[0]  # bbox包含左上，右下2个坐标，但这里转换成长宽更有意义，便于更好的删选
        face.height = bbox[3] - bbox[1]
        print(f'INFO: bbox is {bbox}')
        face.img_id = img.id  # 绑定图片对象
        face.state = 0  # 已经保存了图片, "0:正常，1：禁用, 9: 已经删除"
        face.is_confirmed = True

        random_name = ''.join(random.sample(string.ascii_letters + string.digits, 5))
        # src_name = face.name + '_' + 'face_' + random_name + '.jpg'  # 其实不用包含facename的，这里加上去主要考虑在浏览器中查看
        src_name = 'face_' + random_name + '.jpg'  # 其实不用包含facename的，这里加上去主要考虑在浏览器中查看

        face.src = os.path.join('face', face.name, src_name)  # imagefiled 对应的路径名
        face.save()
        if not os.path.exists(os.path.dirname(face.src.path)):  # 确保路径存在，不存在则创建
            os.makedirs(os.path.dirname(face.src.path))

        save_src(face.src.path, img.src.path, bbox)  # 要保存的人脸路径，照片路径，人脸区域

        print(f'INFO: face name is {face.name}')


# 通过LightRoom人脸识别的方式，保存相关人脸信息
def get_LM_face_info(img):
    print(f'INFO: get_LM_face_info ... ')
    num = 1  # xmp 内容下表从1开始
    is_have_face = True

    exiv_info = Image_pyexiv2(img.src.path)  # 登记图片路径
    xmp = exiv_info.read_xmp()  # 读取元数据，这会返回一个字典
    names = []
    bboxs = []
    while is_have_face:
        item = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Type'.format(num)
        is_have_face = xmp.get(item)
        if is_have_face:
            print(f'INFO: LM face detected')
            idx_name = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Name'.format(num)
            idx_h = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Area/stArea:h'.format(num)
            idx_w = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Area/stArea:w'.format(num)
            idx_x = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Area/stArea:x'.format(num)
            idx_y = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Area/stArea:y'.format(num)
            num += 1

            name = xmp.get(idx_name, 'unknown')
            names.append(name)
            lm_face_area = [xmp.get(idx_x), xmp.get(idx_y), xmp.get(idx_w), xmp.get(idx_h)]  # 0~1 之间的字符
            lm_face_area = np.array(lm_face_area).astype(float)  # 0~1 之间的浮点，中心区域，人脸长，宽
            bbox = face_zoom(lm_face_area, 1, img.src.width, img.src.height)  # 转变成像素值，左上区域和右下区域坐标，跟insightface 保持一致
            bboxs.append(bbox)

    return names, bboxs


# 要保存的人脸路径，照片路径，人脸区域
def save_src(filepath, img_path, bbox):  # bbox 0，1 表示左上整数，2，3表示右下整数
    # if type(img) is str:
    #     img = Image_PIL.open(img)
    # else:
    #     img = img
    # img = cv.imread(img_path)  # 这里不用cv进行读取，理由是如果路径名包含中文，保存就会乱码
    img = Image_PIL.open(img_path)
    # print(f'INFO: face path is {filepath}')
    bbox = np.array(bbox).astype(int)
    if bbox.min() < 0:  # 不完整的人脸
        return
    region = img.crop(bbox)
    region.save(filepath)


def face_zoom(area, ratio, width, height):  # area: 中心坐标，宽度，高度
    [x, y, w, h] = area

    w = w * ratio
    h = h * ratio
    x1 = max(x - w / 2, 0)
    y1 = max(y - h / 2, 0)
    x2 = min(x1 + w, 1)
    y2 = min(y1 + h, 1)
    # print(f'INFO: the face width is {width}, face height is {height}')
    bbox = [x1 * width, y1 * height, x2 * width, y2 * height]

    return bbox  # 这里的bbox 还是浮点型，后续保存图片的时候同意转换
    # return np.array(bbox).astype(int)


def save_face_database(img, face, names, bboxs):  # save face to database

    # 1. 获取人脸名字
    if len(names) == 0:  # 通过LM方式未检测到人脸
        print(f'INFO: there is no LM_face_info detected ... ')
        print(f'INFO: estimated face name based on exist feats now  ... ')
        face_name, sim = get_face_name(face.normed_embedding)  # 通过跟人脸特征库的比较，推理出相关人脸名称

    else:  # 通过LM方式检测到了人脸
        ious = []
        for bbox in bboxs:
            iou = compute_IOU(bbox, face.bbox)  # 计算LM 人脸区域跟insight face 人脸区域的重合度
            ious = np.append(ious, iou)
        idx = ious.argmax()
        # print(f'INFO ious is {ious}')
        # print(f'INFO names is {names}')
        # print(f'INFO: the identified idx is {idx}')
        if ious[idx] > 0.3:  # 重合度超过30%
            face_name = names[idx]
            sim = 1
        else:
            face_name = 'unknown'
            sim = 0
        print(f"\033[1;32m INFO: estimated name is {face_name}, which is from LM \033[0m")

    # get the album info
    random_name = ''.join(random.sample(string.ascii_letters + string.digits, 5))
    if face_name == 'unknown':
        face_name = face_name + '_' + random_name

    face_info_name = 'face_info_' + random_name + '.npy'  # 人脸信息把名字去掉
    src_name = 'face_' + random_name + '.jpg'  # face name with random letters
    face_info = os.path.join('face_info', face_info_name)  # 不按人名进行分类
    face_src = os.path.join('face', src_name)
    # face_info = os.path.join('face_info', face_name, face_info_name)
    # face_src = os.path.join('face', face_name, src_name)

    # 2. 判断人脸相册是否存在该人，不存在则创建,
    album = update_album_database(face_name, face_info, face_src)

    'sys_img/logo_lg.png'

    # 3. 保存人脸信息到数据库
    fc = Face()
    fc.img_id = img.id
    fc.name = face_name
    fc.det_score = face.det_score
    fc.face_score = sim
    # if sim == 1:  # 已经确认是该人了, 更新人脸信息到本地
    if sim > 0.8:  # 概率大于0.8， 基本上可以确认是该人了
        print(f"\033[1;32m INFO: the face name is confirmed, which is {face_name} \033[0m")
        fc.is_confirmed = True
    fc.age = face.age
    fc.gender = face.gender
    fc.det_method = 1  # InsightFace 识别方式

    bbox = np.array(face.bbox).astype(int)
    fc.x = bbox[0]
    fc.y = bbox[1]
    fc.wid = bbox[2] - bbox[0]
    fc.height = bbox[3] - bbox[1]
    # if fc.wid < 100:  # 人脸照片太小，则直接返回，不进行保存
    #     return
    fc.face_info = face_info
    fc.src = face_src

    fc.face_album_id = album.id

    fc.save()

    # if not os.path.exists(os.path.dirname(fc.face_info.path)):
    #     os.makedirs(os.path.dirname(fc.face_info.path))
    # if not os.path.exists(os.path.dirname(fc.src.path)):
    #     os.makedirs(os.path.dirname(fc.src.path))

    return fc


def save_face_info(filepath, face, face_name='unknown'):  # media/face_info/name/file
    fc_info = FaceInfo()
    fc_info.normed_embedding = face.normed_embedding
    fc_info.bbox = face.bbox
    fc_info.kps = face.kps
    fc_info.landmark_2d_106 = face.landmark_2d_106
    fc_info.landmark_3d_68 = face.landmark_3d_68
    fc_info.pose = face.pose

    np.save(filepath, fc_info)  # 保存所有的人脸信息


# encoding: utf-8
def compute_IOU(rec1, rec2):  # 这里的矩形，包括左上角坐标和右下角坐标
    """
    计算两个矩形框的交并比。
    :param rec1: (x0,y0,x1,y1)      (x0,y0)代表矩形左上的顶点，（x1,y1）代表矩形右下的顶点。下同。
    :param rec2: (x0,y0,x1,y1)
    :return: 交并比IOU.
    """
    left_column_max = max(rec1[0], rec2[0])
    right_column_min = min(rec1[2], rec2[2])
    up_row_max = max(rec1[1], rec2[1])
    down_row_min = min(rec1[3], rec2[3])
    # 两矩形无相交区域的情况
    if left_column_max >= right_column_min or down_row_min <= up_row_max:
        return 0
    # 两矩形有相交区域的情况
    else:
        S1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
        S2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])
        S_cross = (down_row_min - up_row_max) * (right_column_min - left_column_max)
        return S_cross / (S1 + S2 - S_cross)


# @app.task
@ shared_task
def upload_face_to_mcs(fc_obj):  # img = self.get_object()  # 获取详情的实例对象
    if not hasattr(fc_obj, 'mcs'):  # 判断是否又对应的mcs存储

        data = upload_file_pay_face(wallet_info, fc_obj.src.path)
        # 调用序列化器进行反序列化验证和转换
        data.update(id=fc_obj.id)
        serializer = McsDetailSerializer(data=data)
        # 当验证失败时,可以直接通过声明 raise_exception=True 让django直接跑出异常,那么验证出错之后，直接就再这里报错，程序中断了就

        result = serializer.is_valid(raise_exception=True)
        print(serializer.errors)  # 查看错误信息

        # 获取通过验证后的数据
        print(serializer.validated_data)  # form -- clean_data
        # 保存数据
        mcs_obj = serializer.save()

        msg = 'success to make a copy into mac, the file_upload_id is %d' % mcs_obj.file_upload_id

    else:
        msg = 'there is already have mac info related to this img: file id is %d' % fc_obj.mcs.file_upload_id

    print(msg)

# @app.task
@ shared_task
# 通过InsightFace 人脸识别的方式，保存相关人脸信息
def save_insight_faces(img):
    print(f'INFO: insight face detecting the face now ... ')
    app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_size=(640, 640))
    image_path = img.src.path

    req_img = cv.imread(image_path)  # 自己用openCV进行读取
    faces = app.get(req_img)  # 使用insight face 获取人脸信息

    names, bboxs = get_LM_face_info(img)  # 从lightroom 中获取人脸信息
    print(f'INFO LM names is {names}')
    for face in faces:
        if face.det_score < 0.3:  # 是人脸的可能性 < 0.4
            continue
        fc_obj = save_face_database(img, face, names, bboxs)  # 保存相关信息到数据库
        save_face_info(fc_obj.face_info.path, face, fc_obj.name)  # 保存人脸信息到磁盘
        save_src(fc_obj.src.path, image_path, face.bbox)  # 保存人脸图片到磁盘
        upload_face_to_mcs(fc_obj)  # update the face to mcs

        # if fc_obj.is_confirmed == 1:  # 如果人脸通过LM识别进行了确认，也就是IOU大于一定的程度
        #     # 5. 更新并保存该人脸所有特征和中心特征到文件系统，并返回结果
        #     fts, cft = save_people_feats(fc_obj.name)
        #
        #     # 6. 更新并保存所有人脸姓名和中心特征到文件系统，并返回结果
        #     all_names, all_fts = save_all_feats()
        #
        #     # 7. 根据计算好的中心向量，更新该人脸所有的相似度
        #     update_face_sim(fc_obj.name, cft)
