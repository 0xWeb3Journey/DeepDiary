import datetime
import numpy as np
import os
import os.path as osp
import glob
import cv2
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image


assert insightface.__version__>='0.7'

if __name__ == '__main__':
    app = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=0, det_size=(640, 640))

    img = ins_get_image('t1')
    faces = app.get(img)
    face = faces[0]
    fc = {'det_score': face.det_score,
          'age': face.age,
          'gender': face.gender,
          'normed_embedding': face.normed_embedding.astype(np.float16),
          'bbox': np.round(face.bbox).astype(np.int16),
          'kps': np.round(face.kps).astype(np.int16),
          'landmark_2d_106': np.round(face.landmark_2d_106).astype(np.int16),
          'landmark_3d_68': np.round(face.landmark_3d_68).astype(np.int16),
          'pose': face.pose.astype(np.float16),
          }
