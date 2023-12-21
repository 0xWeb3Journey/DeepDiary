# utils/views.py
import os
import time

from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet

from deep_diary.settings import MEDIA_ROOT


# parser.add_argument("--run_type", type=str, default='face_maker', help="run type, eg. image, image_flod, video "
#                                                                        "train, face_maker, face_check")
from utilities.pagination import GeneralPageNumberPagination
from utilities.serializers import AdSerializer


def create_output_fold(run_type):
    ## creat a new saving flod
    current_time = time.localtime()
    output_flod = os.path.join(MEDIA_ROOT, 'tmp_outputs',
                               run_type + '_' + time.strftime("%Y_%m_%d_%H_%M_%S", current_time))
    os.makedirs(output_flod, exist_ok=True)
    return output_flod





