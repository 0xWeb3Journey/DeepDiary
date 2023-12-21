import uuid

import numpy as np
from insightface.app import FaceAnalysis

from deep_diary.settings import calib
from library.process.base_processor import ImageProcessor
from utilities.common import trace_function


# from django.core.files import File
# from utils.mcs_storage import upload_file_pay


class FaceProcessor(ImageProcessor):
    # ... 其他方法 ...
    # def __init__(self, image_processor):

    def __init__(self, img=None):
        super().__init__(img)
        self.app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        self.app.prepare(ctx_id=0, det_size=(640, 640), det_thresh=calib['face']['det_threshold'])  # 默认det_thresh=0.5,
        self.enableLM = True
        self.is_need_recognize = True

    @trace_function
    def get(self, *args, **kwargs):
        faces = []
        LMnames = []
        LMbboxs = []
        ins_fcs = self.app.get(self.img_cv2)
        if self.enableLM and self.xmp:  # 通过LM方式检测到了人脸
            LMnames, LMbboxs = self.get_lm_face_info()
        for face in ins_fcs:
            pose = face.pose.astype(np.float16)
            bbox = np.round(face.bbox).astype(np.int16)
            name, face_score = self.get_name(LMnames, LMbboxs, face.bbox)
            if face_score == 1:  # 通过LM方式检测到了人脸
                self.is_need_recognize = False

            fc = {
                'img': None,  # 后续在处理数据库保存的时候再对其赋值
                'profile': name,  # 后续在处理数据库保存的时候再对其赋值
                'det_score': face.det_score,
                'face_score': face_score,
                'is_confirmed': True if face_score == 1 else False,
                # 如果是self.is_need_recognize = True,则需要进行人脸识别，然后对其再次赋值
                'src': self.face_crop(self.img_pil, bbox, name),  # 返回django.core.files.base import File 对象
                'age': face.age,
                'gender': face.gender,
                'embedding': face.normed_embedding.astype(np.float16).tobytes(),
                'pose_x': pose[0],
                'pose_y': pose[1],
                'pose_z': pose[2],
                'x': bbox[0],
                'y': bbox[1],
                'wid': bbox[2] - bbox[0],
                'height': bbox[3] - bbox[1],
            }
            data = {
                'fc': fc,
                'kps': np.round(face.kps).astype(np.int16),
                'landmarks2d': np.round(face.landmark_2d_106).astype(np.int16),
                'landmarks3d': np.round(face.landmark_3d_68).astype(np.int16),
                'profile': name,
            }
            faces.append(data)

        return {
            'face': faces,
        }

    def get_lm_face_info(self):
        print(f'INFO: get_LM_face_info STARTED ... ')
        num = 1  # xmp 内容下表从1开始
        is_have_face = True
        names = []
        bboxs = []
        xmp = self.xmp
        # print(f'INFO: xmp is {json.dumps(xmp, indent=4)}')
        while is_have_face:
            item = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Type'.format(num)
            is_have_face = xmp.get(item, None)
            if is_have_face:
                # print(f'INFO: LM face detected')
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
                bbox = self.face_zoom(lm_face_area, 1, self.img_pil.width,
                                      self.img_pil.height)  # 转变成像素值，左上区域和右下区域坐标，跟insightface 保持一致
                bboxs.append(bbox)
        # print(f'INFO: the LM names is {names}, bbox is {bboxs}')
        print(f'INFO: get_LM_face_info END ... ')

        return names, bboxs

    @staticmethod
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

        return np.array(bbox).astype(int)

    def get_name(self, names, LMbboxs, bbox):
        name = 'unknown_' + str(uuid.uuid4())[:8]  # 生成一个随机的名字
        score = 0
        if len(names) > 0:
            for i in range(len(names)):
                if self.compute_iou(LMbboxs[i], bbox):
                    name = names[i]
                    score = 1
                    break
        print(f'INFO: get_name END ... , the name is {name}')
        return name, score

    @staticmethod
    def compute_iou(rec1, rec2):  # 这里的矩形，包括左上角坐标和右下角坐标
        """
        计算两个矩形框的交并比。
        :param rec1: (x0,y0,x1,y1)      (x0,y0)代表矩形左上的顶点，（x1,y1）代表矩形右下的顶点。下同。
        :param rec2: (x0,y0,x1,y1)
        :return: 交并比IOU.
        """
        iou = 0
        rst = False
        left_column_max = max(rec1[0], rec2[0])
        right_column_min = min(rec1[2], rec2[2])
        up_row_max = max(rec1[1], rec2[1])
        down_row_min = min(rec1[3], rec2[3])
        # 两矩形无相交区域的情况
        if left_column_max >= right_column_min or down_row_min <= up_row_max:
            rst = False
        # 两矩形有相交区域的情况
        else:
            S1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
            S2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])
            S_cross = (down_row_min - up_row_max) * (right_column_min - left_column_max)
            iou = S_cross / (S1 + S2 - S_cross)
            if iou > 0.5:
                rst = True

        print(f'INFO: computed_iou is {iou} ... ')

        return rst
