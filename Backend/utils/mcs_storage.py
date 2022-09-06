import os

from django.test import TestCase

# Create your tests here.

import cv2
import numpy as np

import requests
from PIL import Image
from io import BytesIO
from insightface.app import FaceAnalysis
# from mcs import ContractAPI, McsAPI
from mcs import ContractAPI, McsAPI
from pyexiv2 import Image as Image_pyexiv2

# req_img = cv.imread('https://mcs.filswan.com/#/my_files/detail/0/0/477473')
# print(req_img)

import urllib
from urllib.request import urlopen
import urllib3
import datetime


# img_src = 'https://calibration-ipfs.filswan.com/ipfs/QmSAwRTQkB6pmvhrLQU2j1yhYGLPGPQQeaTgAiajyFdMyE'
from deep_diary.config import wallet_info
from deep_diary.settings import FACE_ROOT
from library.serializers import McsSerializer


def approve_usdc(wallet_info):
    w3_api = ContractAPI(wallet_info['web3_api'])
    w3_api.approve_usdc(wallet_info['wallet_address'],
                        wallet_info['private_key'], "1")


def upload_file_pay(wallet_info, img, store_to_database=True):  # img is an object
    filepath = img.src.path

    wallet_address = wallet_info['wallet_address']
    private_key = wallet_info['private_key']
    web3_api = wallet_info['web3_api']

    w3_api = ContractAPI(web3_api)
    api = McsAPI()
    # upload file to mcs
    filename = os.path.basename(filepath)

    upload_file = api.upload_file(wallet_address, filepath)
    file_data = upload_file["data"]
    payload_cid, source_file_upload_id, nft_uri, file_size, w_cid = file_data['payload_cid'], file_data[
        'source_file_upload_id'], file_data['ipfs_url'], file_data['file_size'], file_data['w_cid']
    # get the global variable


    params = api.get_params()["data"]
    # get filcoin price
    rate = api.get_price_rate()["data"]
    # upload file and pay contract
    tx_hash = w3_api.upload_file_pay(wallet_address, private_key, file_size, w_cid, rate, params)


    # upload nft metadata
    meta_url = api.upload_nft_metadata(wallet_address, filename,
                                       nft_uri, tx_hash, file_size)['data']['ipfs_url']
    # mint nft contract
    tx_hash, token_id = w3_api.mint_nft(wallet_address, private_key, meta_url)
    # update mint info
    mint_info = api.get_mint_info(source_file_upload_id, None, tx_hash, token_id, wallet_address)
    print(mint_info)


    if store_to_database:
        data = {
            "img": img.id,
            "file_upload_id": file_data['source_file_upload_id'],
            "file_name": filename,
            "file_size": file_data['file_size'],
            # "updated_at": updated_at,
            "nft_url": file_data['ipfs_url'],
            "pin_status": 'Pinned',
            "payload_cid": file_data['payload_cid'],
            "w_cid": file_data['w_cid'],
            "status": upload_file["status"],
            "deal_success": True,
            "is_minted": True,
            "token_id": token_id,
            "mint_address": mint_info['data']['mint_address'],
            "nft_tx_hash": tx_hash,

        }
        # 调用序列化器进行反序列化验证和转换
        serializer = McsSerializer(data=data)
        # 当验证失败时,可以直接通过声明 raise_exception=True 让django直接跑出异常,那么验证出错之后，直接就再这里报错，程序中断了就

        result = serializer.is_valid(raise_exception=True)
        print("验证结果:%s" % result)

        print(serializer.errors)  # 查看错误信息

        # 获取通过验证后的数据
        print(serializer.validated_data)  # form -- clean_data
        # 保存数据
        mcs_obj = serializer.save()
    return source_file_upload_id, nft_uri


def list_files(wallet_info):
    wallet_address = wallet_info['wallet_address']

    api = McsAPI()
    return api.get_user_tasks_deals(wallet_address)


def file_detail(wallet_info, source_file_upload_id):
    wallet_address = wallet_info['wallet_address']
    web3_api = wallet_info['web3_api']
    api = McsAPI()
    file_detail = api.get_deal_detail(wallet_address, source_file_upload_id)

    return file_detail


# 网络上图片的地址
def save_mcs_file(img_src, filepath):

    start = datetime.datetime.now()
    response = requests.get(img_src)
    end = datetime.datetime.now()
    print(f'totally time is {end}-{start}')
    image = Image.open(BytesIO(response.content))
    image.save(filepath)
#
# app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
# app.prepare(ctx_id=0, det_size=(640, 640))
# image_path = '9.jpg'


# URL到图片
def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.request.urlopen(url)
    # bytearray将数据转换成（返回）一个新的字节数组
    # asarray 复制数据，将结构化数据转换成ndarray
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    # cv2.imdecode()函数将数据解码成Opencv图像格式
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # return the image
    return image


# file_path = FACE_ROOT
# # # approve_usdc(wallet_info)
# #
# # start = datetime.datetime.now()
# #
# upload_file_pay(wallet_info, file_path)
# mcs_files = list_files(wallet_info)
# # file_detail = file_detail(wallet_info, 477557)
#
# end = datetime.datetime.now()
#
# print(end-start)


