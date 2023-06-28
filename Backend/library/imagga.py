# Create your tests here.
from deep_diary.settings import cfg
import requests
from requests.auth import HTTPBasicAuth

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


def imagga_get(image_url, endpoint, query_add=None, upload_id=False):  # query must include the 'image_url'
    if query_add is None:
        query_add = {}

    response = requests.get(
        '%s/%s?image_url=%s' % (ENDPOINT, endpoint, image_url),
        # '%s/%s' % (ENDPOINT, endpoint),
        auth=(API_KEY, API_SECRET),
        params=query_add)

    return response.json()

