# Create your tests here.
from deep_diary.settings import cfg
import requests
from requests.auth import HTTPBasicAuth

from utilities.common import trace_function

###
# API Credentials
API_KEY = cfg['imagga']['api_key']  # Set API key here
API_SECRET = cfg['imagga']['api_secret']  # Set API secret here
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


@trace_function
def imagga_post(img_path, endpoint, query=None):  # using the loca img

    if query is None:
        query = {}
    query = query.update(query)
    response = requests.post(
        '%s/%s' % (ENDPOINT, endpoint),
        auth=(API_KEY, API_SECRET),
        files={'image': open(img_path, 'rb')},
        params=query)

    return response.json()


@trace_function
def imagga_get(image_url, endpoint, query=None, upload_id=False):  # query must include the 'image_url'
    if query is None:
        query = {}
    query = query.update(query)
    response = requests.get(
        '%s/%s?image_url=%s' % (ENDPOINT, endpoint, image_url),
        # '%s/%s' % (ENDPOINT, endpoint),
        auth=(API_KEY, API_SECRET),
        params=query)

    return response.json()


def imagga_api_call(img_source, endpoint='tags', query=None, method='get'):
    """通用函数用于调用Imagga API"""

    if method == 'get':
        return imagga_get(img_source, endpoint, query=query)
    elif method == 'post':
        return imagga_post(img_source, endpoint, query=query)
    else:
        return None
