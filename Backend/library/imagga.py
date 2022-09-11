# Create your tests here.
import os

import django

from deep_diary.config import api_key, api_secret

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deep_diary.settings')
django.setup()

import requests
from requests.auth import HTTPBasicAuth

###
# API Credentials
API_KEY = api_key  # Set API key here
API_SECRET = api_secret  # Set API secret here
###
ENDPOINT = 'https://api.imagga.com/v2'
FILE_TYPES = ['png', 'jpg', 'jpeg', 'gif']


class ArgumentException(Exception):
    pass


if API_KEY == 'YOUR_API_KEY' or \
        API_SECRET == 'YOUR_API_SECRET':
    raise ArgumentException('You haven\'t set your API credentials. '
                            'Edit the script and set them.')

auth = HTTPBasicAuth(API_KEY, API_SECRET)


def post_img_tags(img_obj, threshold=30):
    img_path = img_obj.src.path
    tag_result = requests.post(
        '%s/colors' % ENDPOINT,
        auth=(api_key, api_secret),
        files={'image': open(img_path, 'rb')})

    tag_result = tag_result.json()


def tag_image_post(img_path, upload_id=False, verbose=False, language='en'):
    # Using the local img through post mathod to get the tags,

    tagging_query = {
        'verbose': verbose,
        'language': language
    }
    tagging_response = requests.post(
        '%s/tags' % ENDPOINT,
        auth=(api_key, api_secret),
        files={'image': open(img_path, 'rb')},
        params=tagging_query)

    return tagging_response.json()


def tag_image(image, upload_id=False, verbose=False, language='en'):
    # Using the content id and the content parameter,
    # make a GET request to the /tagging endpoint to get
    # image tags
    tagging_query = {
        'image_upload_id' if upload_id else 'image_url': image,
        'verbose': verbose,
        'language': language
    }
    tagging_response = requests.get(
        '%s/tags' % ENDPOINT,
        auth=auth,
        params=tagging_query)

    return tagging_response.json()


def extract_colors(image, upload_id=False):
    colors_query = {
        'image_upload_id' if upload_id else 'image_url': image,
    }

    colors_response = requests.get(
        '%s/colors' % ENDPOINT,
        auth=auth,
        params=colors_query)

    return colors_response.json()
