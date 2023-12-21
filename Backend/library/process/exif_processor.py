import bisect
from datetime import datetime

from deep_diary.settings import calib
from library.gps import GPS_format, GPS_to_coordinate, GPS_get_address
from library.process.base_processor import ImageProcessor
from utilities.common import trace_function


# from django.core.files import File
# from utils.mcs_storage import upload_file_pay


class ExifProcessor(ImageProcessor):
    # ... 其他方法 ...
    def __init__(self, img=None):
        super().__init__(img)
    @trace_function
    def get(self, *args, **kwargs):
        if not self.exif:
            return None
        exif = {
            'date': self.get_date(),
            'addr': self.get_addr(),
            'eval': self.get_eval(),
            'base': self.get_base(),
            'tag': self.get_tags(),
        }
        # print(f'exif is {exif}')
        return exif

    @staticmethod
    def resolve_date(date_str):
        # 解析日期的静态方法
        if not date_str:
            date_str = '1970:01:01 00:00:00'
        tt = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
        date = {
            'capture_date': tt.strftime("%Y-%m-%d"),
            'capture_time': tt.strftime("%H:%M:%S"),
            'year': str(tt.year).rjust(2, '0'),
            'month': str(tt.month).rjust(2, '0'),
            'day': str(tt.day).rjust(2, '0'),
            'is_weekend': tt.weekday() >= 5,
            'earthly_branches': bisect.bisect_right(calib['hour_slot'], tt.hour) - 1,
        }
        return date

    @trace_function
    def get_date(self):

        # deal with timing
        date_str = self.exif.get('Exif.Photo.DateTimeOriginal',
                                 '1970:01:01 00:00:00') if self.exif else '1970:01:01 00:00:00'

        date_dict = self.resolve_date(date_str)  # return the date instance
        return date_dict

    @trace_function
    def get_addr(self):

        exif = self.exif

        print(f'INFO: get_addr----->exif is true ')

        longitude = GPS_format(exif.get('Exif.GPSInfo.GPSLongitude', None))
        latitude = GPS_format(exif.get('Exif.GPSInfo.GPSLatitude', None))
        altitude = exif.get('Exif.GPSInfo.GPSAltitude', None)  # 根据高度信息，最终解析成float 格式
        if type(altitude) == str:
            alt = altitude.split('/')
            altitude = float(alt[0]) / float(alt[1])

        is_located = True if longitude and latitude else False

        long_lati = None
        if is_located:
            long_lati = GPS_to_coordinate(longitude, latitude)
            # TODO: need update the lnglat after transform the GPS info
            longitude = round(long_lati[0], 6)  # only have Only 6 digits of precision for AMAP
            latitude = round(long_lati[1], 6)
            # print(f'instance.longitude {addr.longitude},instance.latitude {addr.latitude}')
            long_lati = f'{long_lati[0]},{long_lati[1]}'  # change to string
            print(f'INFO: get_addr----->long_lati is {long_lati}')

        location, district, city, province, country = GPS_get_address(long_lati)

        addr = {
            'longitude_ref': exif.get('Exif.GPSInfo.GPSLongitudeRef', 'E'),
            'longitude': longitude,
            'latitude_ref': exif.get('Exif.GPSInfo.GPSLatitudeRef', 'N'),
            'latitude': latitude,
            'altitude_ref': float(exif.get('Exif.GPSInfo.GPSAltitudeRef', 0.0)),
            'altitude': altitude,
            'is_located': is_located,
            'country': country,
            'province': province,
            'city': city,
            'district': district,
            'location': location,
        }

        return addr

    @trace_function
    def get_eval(self):
        rate = {
            'rating': int(self.xmp.get('Xmp.xmp.Rating', 0)),
        }
        return rate

    @trace_function
    def get_base(self):

        exif = self.exif
        iptc = self.iptc
        xmp = self.xmp
        img_pil = self.img_pil

        wid = int(exif.get('Exif.Image.ImageWidth', 0)) if exif and int(exif.get('Exif.Image.ImageWidth', 0)) else int(
            img_pil.width)  # 其实本身已经是int类型的了
        height = int(exif.get('Exif.Image.ImageLength', 0)) if exif and int(
            exif.get('Exif.Image.ImageLength', 0)) else int(img_pil.height)  # 其实本身已经是int类型的了
        print(wid, height)
        aspect_ratio = height / wid if wid != 0 else 0
        camera_brand = exif.get('Exif.Image.Make', '') if exif else ''
        camera_model = exif.get('Exif.Image.Model', '') if exif else ''

        title = iptc.get('iptc.Application2.ObjectName') if iptc else ''
        caption = iptc.get('Iptc.Application2.Caption') if iptc else ''

        label = xmp.get('Xmp.xmp.Label') if xmp else ''

        base = {
            'wid': wid,
            'height': height,
            'aspect_ratio': aspect_ratio,
            'camera_brand': camera_brand,
            'camera_model': camera_model,
            'title': title,
            'caption': caption,
            'label': label,
            'is_exist': True,
        }
        return base

    @trace_function
    def get_tags(self):
        return self.iptc.get('Iptc.Application2.Keywords', []) if self.iptc else []