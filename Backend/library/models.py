import os
from datetime import datetime

from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Value, F, Subquery, OuterRef
# Create your models here.
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from taggit.managers import TaggableManager

from deep_diary.settings import calib
from project.models import Issue

# Create your models here.
from user_info.models import Profile

STATE_OPTION = (
    (0, "正常"),
    (1, "禁用"),
    (9, "已经删除"),
)
SEX_OPTION = (
    (0, "男"),
    (1, "女"),
    (2, "保密"),
)

DET_METHOD_OPTION = (
    (0, "Lightroom"),
    (1, "InsightFace"),
    (2, "Others"),
)


def user_directory_path(instance, filename):  # dir struct MEDIA/user/subfolder/file
    sub_folder = "img"
    instance.name = filename
    instance.type = filename.split('.')[-1]
    if not instance.user.username:
        instance.user.username = 'unauthorized'
    # os.path.join will be wrong: blue\img\1970\1\1\avatar.jpg
    # user_img_path = os.path.join(instance.user.username, sub_folder, date_path, filename)
    user_img_path = '{0}/{1}/{2}'.format(instance.user.username, sub_folder, filename)
    print('照片存放路径为：' + user_img_path)  # dir struct MEDIA/user/subfolder/file

    return user_img_path


def category_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'category/{0}/{1}'.format(instance.name, filename)


def face_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'face/{0}'.format(filename)


class Img(models.Model):
    # 所属用户
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="所属用户", default=1, related_name='imgs')
    # 230624 新增多对多关系
    profiles = models.ManyToManyField(Profile, through='Face', verbose_name="相关用户", related_name='face_imgs')
    src = models.ImageField(upload_to=user_directory_path,
                            verbose_name="照片路径",
                            help_text='保存到本地路径',
                            null=True, blank=True,
                            default='sys_img/logo_lg.png',
                            )
    url = models.ImageField(upload_to=user_directory_path,
                            verbose_name="照片路径",
                            help_text='保存到网络中的路径',
                            null=True, blank=True,
                            default='sys_img/logo_lg.png',
                            )
    # image = ProcessedImageField(upload_to=user_directory_path,    # 使用这个字段，会导致图像元数据丢失
    #                             processors=[ResizeToFit(width=1500, height=1500)],
    #                             format='JPEG',
    #                             options={'quality': 90},
    #                             verbose_name='图片',
    #                             help_text='请选择需要上传的图片',
    #                             null=True, blank=True,
    #                             default='sys_img/logo_lg.png'
    #                             )
    thumb = ImageSpecField(source='src',
                           # processors=[ResizeToFill(300, 300)],
                           processors=[ResizeToFit(width=200, height=200)],
                           # processors=[Thumbnail(width=300, height=300, anchor=None, crop=None, upscale=None)],
                           format='JPEG',
                           options={'quality': 80},
                           )

    name = models.CharField(default='unnamed', max_length=40, null=True, blank=True, unique=True,
                            verbose_name="图片名", help_text='')  # unique=False, 方便调试
    type = models.CharField(max_length=10, null=True, blank=True, verbose_name="图片格式", help_text='图片格式')
    wid = models.IntegerField(default=0, blank=True, verbose_name="图片宽度", help_text='图片宽度')
    height = models.IntegerField(default=0, blank=True, verbose_name="图片高度", help_text='图片高度')
    aspect_ratio = models.DecimalField(default=0.0, max_digits=3, decimal_places=2, null=True, blank=True,
                                       verbose_name="长宽比")

    ## 标签属性: label
    title = models.CharField(max_length=20, null=True, blank=True, verbose_name="图片标题", help_text='图片标题')
    caption = models.CharField(max_length=100, null=True, blank=True, verbose_name="图片描述", help_text='图片描述')
    label = models.CharField(max_length=20, null=True, blank=True, verbose_name="图片说明", help_text='图片说明')
    tags = TaggableManager(blank=True, verbose_name="照片标签", help_text='照片标签', related_name='imgs')
    embedding = models.BinaryField(null=True, blank=True, verbose_name='图片特征',
                                   help_text='图片特征向量，用于以文搜图，以图搜图')

    camera_brand = models.CharField(max_length=30, null=True, blank=True, verbose_name="相机品牌", help_text='相机品牌')
    camera_model = models.CharField(max_length=30, null=True, blank=True, verbose_name="相机型号", help_text='相机型号')

    # 数据库更新日期
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="首次创建的时间", help_text='首次创建的时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最后更新的时间", help_text='最后更新的时间')

    def __str__(self):
        # 判断是否存在address这个属性
        if hasattr(self, 'address'):
            location = self.address.location
        else:
            location = 'No GPS'
        return fr'<div class ="lightGallery-captions" > <h4> Photo by -  <a href="https://www.deep-diary.com" >{self.user.name} </a>  </h4> <p> Location -  {location} </p> </div>'
        # return f'Name: {self.pk}_{self.name}'

    def to_dict(self):
        return {'id': self.id,
                'src': self.src,
                }

    @property  # 表示这个函数不能有参数
    def custom_face(self):
        queryset = self.face.all()  # 获取所有子对象
        #  "name": "face/unknown/blue_1v6aCXIc.jpg"
        # ret = [{"id": item.id, "name": item.name, "face": f'{item.face.path}'} for item in queryset]   # 不报错
        ret = [{"id": item.id, "name": item.name, "face": item.face.path} for item in queryset]  # 可能报错
        return ret

    @staticmethod
    def get_attr_nums(name):
        # img = Category.objects.filter(name=name).first()
        # if not img:
        #     # if there is no record in the database, then return []
        #     return []
        rst = Img.objects.annotate(value=Count(name)).values_list('value', flat=True).distinct().order_by(
            '-value'),
        # 这里如果不加rst[0]，则返回有2个中括号[[]]
        return rst[0]

    @staticmethod
    def get_filtered_attr_nums(qs, name):
        # qs = Img.objects.filter(id__in=qs)
        rst = qs.annotate(value=Count(name)).values('value').distinct().order_by(
            '-value'),
        # 这里如果不加rst[0]，则返回有2个中括号[[]]
        return rst[0]

    class Meta:
        ordering = ('-created_at',)
        get_latest_by = 'id'


class Stat(models.Model):
    """图片状态属性"""
    img = models.OneToOneField(
        Img,
        related_name='stats',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    is_publish = models.BooleanField(blank=True, default=True, verbose_name="是否公开", help_text='是否公开')
    is_path_exist = models.BooleanField(blank=True, default=True, verbose_name="路径是否存在",
                                        help_text='路径是否存在')
    is_deleted = models.BooleanField(blank=True, default=False, verbose_name="是否删除", help_text='是否删除')
    is_get_info = models.BooleanField(blank=True, default=False, verbose_name="是否提取了图片元数据",
                                      help_text='是否提取了图片元数据')
    is_store_mcs = models.BooleanField(blank=True, default=False, verbose_name="是否已经保存到mcs",
                                       help_text='是否已经保存到mcs')
    is_auto_tag = models.BooleanField(blank=True, default=False, verbose_name="是否已经完成自动标注",
                                      help_text='是否已经完成自动标注')
    is_get_color = models.BooleanField(blank=True, default=False, verbose_name="是否完成颜色提取",
                                       help_text='是否完成颜色提取')
    is_get_cate = models.BooleanField(blank=True, default=False, verbose_name="是否完成自动分类",
                                      help_text='是否完成自动分类')
    is_face = models.BooleanField(blank=True, default=False, verbose_name="是否完成人脸识别",
                                  help_text='是否完成人脸识别')
    is_object = models.BooleanField(blank=True, default=False, verbose_name="是否完成目标识别",
                                    help_text='是否完成目标识别')
    is_get_caption = models.BooleanField(blank=True, default=False, verbose_name="是否完成了图转文",
                                         help_text='是否完成了图转文')
    is_get_feature = models.BooleanField(blank=True, default=False, verbose_name="是否完成图片特征的提取",
                                         help_text='是否完成了图转文')
    is_get_clip_classification = models.BooleanField(blank=True, default=False, verbose_name="是否完成图片clip分类",
                                                     help_text='是否完成图片clip分类')


class Category(MPTTModel):
    """图片分类"""
    imgs = models.ManyToManyField(to=Img,
                                  through='ImgCategory',
                                  through_fields=('category', 'img'),  # category need comes first
                                  blank=True,
                                  help_text='对图片按应用进行分类',
                                  default=None,
                                  related_name='categories')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='categories')
    #  unique=True ---》 change to unique together
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="图片类别",
                            help_text='图片按应用进行划分')
    level = models.PositiveIntegerField(default=0, editable=False)

    # TODO: add a condition field to descript the category, which could be a=1&b=2&c=3, or a=1|b=2|c=3,
    #  then the condition could be used to filter the imgs and defined by the user
    logic = models.TextField(blank=True, null=True, verbose_name="分类逻辑", help_text='用于用户定义逻辑')
    description = models.TextField(blank=True, null=True, verbose_name="分类描述", help_text='用于用户定义描述')

    is_leaf = models.BooleanField(default=False, verbose_name="是否叶子节点", help_text='是否叶子节点')
    is_root = models.BooleanField(default=False, verbose_name="是否根节点", help_text='是否根节点')
    # is_active = models.BooleanField(default=True, verbose_name="是否有效", help_text='是否有效')
    is_delete = models.BooleanField(default=False, verbose_name="是否删除", help_text='是否删除')

    # type = models.CharField(max_length=20, default='category', blank=True, verbose_name="分类类型",
    #                         help_text='分类类型')
    # value = models.CharField(max_length=50, null=True, blank=True, verbose_name="类型值", help_text='类型值')
    # numeric_value = models.IntegerField(null=True, blank=True, verbose_name="数值类型值", help_text='数值类型值')

    avatar = models.ImageField(upload_to=user_directory_path,
                               verbose_name="分类相册封面",
                               help_text='分类相册封面',
                               null=True, blank=True,
                               default='sys_img/logo_lg.png',
                               )

    avatar_thumb = ImageSpecField(source='avatar',
                                  processors=[ResizeToFill(300, 300)],
                                  # processors=[ResizeToFit(width=400, height=400)],
                                  # processors=[Thumbnail(width=400, height=400, anchor=None, crop=None, upscale=None)],
                                  format='JPEG',
                                  options={'quality': 80},
                                  )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="首次创建的时间", help_text='首次创建的时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最后更新的时间", help_text='最后更新的时间')

    class Meta:
        # ordering = ['-id']
        unique_together = ('parent', 'name',)

    def __str__(self):
        return f'{self.pk}_{self.name}'

    @staticmethod
    def get_cate_children(name, level=0):

        category = Category.objects.filter(name=name).first()
        if not category:
            # if there is no record in the database, then return []
            return []

        if level <= 1:  # represent the first level
            # rst = children.annotate(value=F('name')).\
            #     values('name', 'value').distinct().order_by('-value'),
            rst = category.get_children().annotate(value=Count('imgs')). \
                values('name', 'value').distinct().order_by('-value'),
        else:
            rst = category.get_descendants().filter(level=level).annotate(
                value=Count('imgs')).values('name',
                                            'value').distinct().order_by('-value'),
        # 这里如果不加rst[0]，则返回有2个中括号[[]]
        # print(rst[0])
        return rst[0]  # or rst[0]

    @staticmethod
    def get_filtered_cate_children(queryset, name, level=0):

        category = Category.objects.filter(name=name).first()
        if not category:
            # if there is no record in the database, then return []
            return []

        if level <= 1:  # represent the first level
            # rst = children.annotate(value=F('name')).\
            #     values('name', 'value').distinct().order_by('-value'),
            rst = category.get_children().filter(imgs__in=queryset).annotate(value=Count('imgs')).distinct(). \
                values('name', 'value').order_by('-value'),
        else:
            # get_descendants = category.get_descendants()
            # print(len(get_descendants))
            # obj_level = category.get_descendants().filter(level=level)
            # print(len(obj_level))
            # obj_level_in_imgs = obj_level.filter(imgs__in=queryset)
            # print(len(obj_level_in_imgs))
            # .exclude(name='[]').exclude(name__isnull=True)
            rst = category.get_descendants().filter(level=level).filter(imgs__in=queryset).annotate(
                value=Count('imgs')).distinct().values('name', 'value').order_by('-value'),
        # 这里如果不加rst[0]，则返回有2个中括号[[]]
        # print('get_filtered_cate_children:', len(rst))
        return rst[0]  # or rst[0]

    def get_cate_children_loop(self, name, level=0):
        rst = None
        # 打印当前位置名称和级别
        print(f"{'    ' * level}{self.name}")
        # 获取子级位置
        children = Category.objects.get(name=name).get_children()
        # rst = children.annotate(value=Count('imgs')).values('name', 'value').distinct().order_by('-value'),
        # 递归查询子级位置
        for child in children:
            rst = self.get_cate_children_loop(child, level + 1)
        return rst


class ImgCategory(models.Model):
    img = models.ForeignKey(Img, on_delete=models.CASCADE, related_name='imgcategories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='imgcategories')
    confidence = models.FloatField(default=0, null=True, blank=True, verbose_name="categories_percentage",
                                   help_text='categories_percentage')  # seems no necessary to use
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="首次创建的时间", help_text='首次创建的时间')

    def __str__(self):
        return f'{self.img.id}_{self.category}'


class ImgMcs(models.Model):
    id = models.OneToOneField(
        Img,
        related_name='img_mcs',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    file_upload_id = models.IntegerField(default=0, null=True, blank=True, verbose_name="up load file id",
                                         help_text='up load file id')
    file_name = models.CharField(max_length=40, null=True, blank=True, verbose_name="file name", help_text='file name')
    file_size = models.IntegerField(default=0, null=True, blank=True, verbose_name="file_size", help_text='file_size')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="updated_at", help_text='updated_at')

    nft_url = models.URLField(
        default='https://calibration-ipfs.filswan.com/ipfs/QmQzPDUheTnFYA7HanxwCLw3QrR7choBvh8pswF4LgxguV', null=True,
        blank=True, verbose_name="NFT 站点", help_text='相当于一个图片源，可以展示图片')
    pin_status = models.CharField(max_length=8, null=True, blank=True, verbose_name="pin_status",
                                  help_text='pin_status')
    payload_cid = models.CharField(max_length=80, null=True, blank=True, verbose_name="payload_cid",
                                   help_text='payload_cid')
    w_cid = models.CharField(max_length=100, null=True, blank=True, verbose_name="w_cid", help_text='w_cid')
    status = models.CharField(max_length=8, null=True, blank=True, verbose_name="status", help_text='status')

    deal_success = models.BooleanField(default=False, blank=True, verbose_name="deal_success", help_text='deal_success')
    is_minted = models.BooleanField(default=False, blank=True, verbose_name="is_minted", help_text='is_minted')
    token_id = models.CharField(max_length=8, null=True, blank=True, verbose_name="token_id", help_text='token_id')
    mint_address = models.CharField(max_length=80, null=True, blank=True, verbose_name="mint_address",
                                    help_text='mint_address')
    nft_tx_hash = models.CharField(max_length=80, null=True, blank=True, verbose_name="nft_tx_hash",
                                   help_text='nft_tx_hash')

    def __str__(self):
        return self.id.name


class Address(models.Model):
    img = models.OneToOneField(
        Img,
        related_name='address',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    ## 地点属性:location
    is_located = models.BooleanField(default=False, blank=True, verbose_name="是否有GPS 信息",
                                     help_text='是否有GPS 信息')
    longitude_ref = models.CharField(default='E', max_length=5, null=True, blank=True, verbose_name="东西经",
                                     help_text='东西经')
    longitude = models.FloatField(default=0.0, max_length=20, null=True, blank=True, verbose_name="经度",
                                  help_text='经度')
    latitude_ref = models.CharField(default='N', max_length=5, null=True, blank=True, verbose_name="南北纬",
                                    help_text='南北纬')
    latitude = models.FloatField(default=0.0, max_length=20, null=True, blank=True, verbose_name="纬度",
                                 help_text='纬度')
    altitude_ref = models.FloatField(default=0.0, max_length=5, null=True, blank=True, verbose_name="参考高度",
                                     help_text='参考高度')
    altitude = models.FloatField(default=0.0, max_length=20, null=True, blank=True, verbose_name="高度",
                                 help_text='高度')
    location = models.CharField(default='No GPS', max_length=50, null=True, blank=True, verbose_name="拍摄地",
                                help_text='拍摄地')
    district = models.CharField(default='No GPS', max_length=20, null=True, blank=True, verbose_name="拍摄区县",
                                help_text='拍摄区县')
    city = models.CharField(default='No GPS', max_length=20, null=True, blank=True, verbose_name="拍摄城市",
                            help_text='拍摄城市')
    province = models.CharField(default='No GPS', max_length=20, null=True, blank=True, verbose_name="拍摄省份",
                                help_text='拍摄省份')
    country = models.CharField(default='No GPS', max_length=20, null=True, blank=True, verbose_name="拍摄国家",
                               help_text='拍摄国家')

    def __str__(self):
        return self.img.name


class Date(models.Model):
    EARTHLY_BRANCHES_OPTION = (
        (0, "凌晨"),
        (1, "早上"),
        (2, "上班"),
        (3, "晚上"),
        (4, "深夜"),
    )

    HOLIDAY_OPTION = (
        (0, "元旦"),
        (1, "春节"),
        (2, "元宵节"),
        (3, "情人节"),
        (4, "妇女节"),
        (5, "清明节"),
        (6, "劳动节"),
        (7, "端午节"),
        (8, "儿童节"),
        (9, "七夕节"),
        (10, "中秋节"),
        (11, "国庆节"),
        (12, "生日"),
        (13, "结婚纪念日"),
    )
    img = models.OneToOneField(
        Img,
        related_name='dates',
        on_delete=models.CASCADE,
        primary_key=True,
    )

    year = models.IntegerField(default=1970, blank=True, verbose_name="拍摄年", help_text='拍摄年')
    month = models.IntegerField(default=1, blank=True, verbose_name="拍摄月", help_text='拍摄月')
    day = models.IntegerField(default=1, blank=True, verbose_name="拍摄日", help_text='拍摄日')
    capture_date = models.DateField(null=True, blank=True, verbose_name="拍摄日期", help_text='拍摄日期')
    capture_time = models.TimeField(null=True, blank=True, verbose_name="拍摄时间", help_text='拍摄时间')
    earthly_branches = models.SmallIntegerField(choices=EARTHLY_BRANCHES_OPTION, null=True, blank=True, default=0,
                                                verbose_name="时间段",
                                                help_text="0: 凌晨，0~5;1: 早上，5~8;  2: 上班，8~17; 3. 晚上，17~21; 4: 深夜,21~24")
    is_weekend = models.BooleanField(null=True, blank=True, verbose_name="是否为周末", help_text='是否为周末')
    # 法定节假日类型(法定节假日往往会有一些不一样的记忆)
    holiday_type = models.SmallIntegerField(choices=HOLIDAY_OPTION, null=True, blank=True, default=0,
                                            verbose_name="节假日",
                                            help_text="法定节假日，纪念日，生日")
    digitized_date = models.DateTimeField(null=True, blank=True, verbose_name="照片修改日期", help_text='照片修改日期')

    def __str__(self):
        return self.img.name


class Evaluate(models.Model):
    FLAG_OPTION = (
        (0, "无旗标"),
        (1, "选中旗标"),
        (2, "排除旗标"),
    )
    img = models.OneToOneField(
        Img,
        related_name='evaluates',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    flag = models.SmallIntegerField(default=0, choices=FLAG_OPTION, null=True, blank=True, verbose_name="旗标",
                                    help_text="0：无旗标，1：选中旗标，2，排除旗标")
    rating = models.IntegerField(default=0, null=True, blank=True, verbose_name="星标等级", help_text='星标等级')
    total_views = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="照片浏览量",
                                              help_text='照片浏览量')
    likes = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="点赞个数", help_text='点赞个数')

    def __str__(self):
        return self.img.name


class Color(models.Model):
    img = models.OneToOneField(
        Img,
        related_name='colors',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    color_variance = models.IntegerField(default=0, null=True, blank=True, verbose_name="color_variance",
                                         help_text='a number that shows how varied the colors in the image are')
    object_percentage = models.FloatField(default=0, null=True, blank=True, verbose_name="object_percentage",
                                          help_text='a floating point number that shows what part of the image '
                                                    'is taken by the main object (as a percent from 0 to 100)')
    color_percent_threshold = models.FloatField(default=0, null=True, blank=True, verbose_name="object_percentage",
                                                help_text='colors with `percentage` value lower than this number '
                                                          'won’t be included in the response')

    def __str__(self):
        return self.img.name


class ColorItem(models.Model):
    r = models.IntegerField(default=0, null=True, blank=True, verbose_name="red color",
                            help_text='numbers between 0 and 255 that represent the red, components of the color')
    g = models.IntegerField(default=0, null=True, blank=True, verbose_name="green color",
                            help_text='numbers between 0 and 255 that represent the green components of the color')
    b = models.IntegerField(default=0, null=True, blank=True, verbose_name="blue color",
                            help_text='numbers between 0 and 255 that represent the  blue components of the color')

    closest_palette_color_html_code = models.CharField(max_length=8, null=True, blank=True,
                                                       verbose_name="palette_color_html_code",
                                                       help_text='palette_color_html_code')

    closest_palette_color = models.CharField(max_length=30, null=True, blank=True, verbose_name="palette_color",
                                             help_text='palette_color')

    closest_palette_color_parent = models.CharField(max_length=30, null=True, blank=True,
                                                    verbose_name="palette_color_parent",
                                                    help_text='palette_color_parent')

    closest_palette_distance = models.FloatField(default=0, null=True, blank=True,
                                                 verbose_name='closest_palette_color_parent',
                                                 help_text='how close this color is to the one under the `closest_palette_color` key')

    percent = models.FloatField(default=0, null=True, blank=True, verbose_name="object_percentage",
                                help_text='a floating point number that shows what part of the image '
                                          'is taken by the main object (as a percent from 0 to 100)')

    html_code = models.CharField(max_length=8, null=True, blank=True, verbose_name="palette_color_html_code",
                                 help_text='palette_color_html_code')

    def __str__(self):
        return self.closest_palette_color_parent


class ColorBackground(ColorItem):
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='background',
                              verbose_name="BackgroundColor")


class ColorForeground(ColorItem):
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='foreground',
                              verbose_name="ColorForeground")


class ColorImg(ColorItem):
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='image',
                              verbose_name="ColorImg")


class Face(models.Model):
    img = models.ForeignKey(Img, null=True, on_delete=models.CASCADE, verbose_name="所属照片", related_name='faces')
    profile = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE, verbose_name="所属人脸相册",
                                related_name='faces')

    is_confirmed = models.BooleanField(blank=True, default=False, verbose_name="人脸是否已确认",
                                       help_text='请对人脸名字进行确认')
    det_score = models.FloatField(null=True, blank=True, verbose_name="是人脸的概率", help_text='是人脸的概率')
    face_score = models.FloatField(null=True, blank=True, verbose_name="是这个人的概率", help_text='是这个人的概率')
    age = models.SmallIntegerField(null=True, blank=True, verbose_name="人脸的年龄，用于训练",
                                   help_text='人脸的年龄，用于训练')
    gender = models.SmallIntegerField(choices=SEX_OPTION, default=2, blank=True, verbose_name="性别",
                                      help_text="0:女，1：男, 2： 保密")
    embedding = models.BinaryField(null=True, blank=True, verbose_name='人脸特征',
                                   help_text='已识别的人脸特征向量')
    src = models.ImageField(upload_to=face_directory_path,
                            verbose_name="人脸路径",
                            help_text='保存到本地的人脸路径',
                            null=True, blank=True,
                            default='sys_img/unknown.jpg',
                            )
    url = models.ImageField(upload_to=face_directory_path,
                            verbose_name="人脸路径",
                            help_text='保存到网络的人脸路径',
                            null=True, blank=True,
                            default='sys_img/unknown.jpg',
                            )
    thumb = ImageSpecField(source='src',
                           processors=[ResizeToFill(300, 300)],
                           format='JPEG',
                           options={'quality': 80})
    x = models.IntegerField(null=True, blank=True, verbose_name="左上角x坐标", help_text='人脸左上角x坐标')
    y = models.IntegerField(null=True, blank=True, verbose_name="左上角y坐标", help_text='人脸左上角y坐标')
    wid = models.IntegerField(null=True, blank=True, verbose_name="宽度", help_text='人脸宽度')
    height = models.IntegerField(null=True, blank=True, verbose_name="高度", help_text='人脸高度')

    pose_x = models.FloatField(null=True, blank=True, verbose_name="俯仰（Pitch）角度",
                               help_text='俯仰角描述物体绕其横轴旋转的角度')
    pose_y = models.FloatField(null=True, blank=True, verbose_name="偏航（Yaw）角度",
                               help_text='偏航角描述物体绕其竖轴旋转的角度')
    pose_z = models.FloatField(null=True, blank=True, verbose_name="翻滚（Roll）角度",
                               help_text='翻滚角描述物体绕其纵轴旋转的角度')

    det_method = models.SmallIntegerField(choices=DET_METHOD_OPTION, null=True, blank=True, default=0,
                                          verbose_name="检测方法",
                                          help_text="人脸检测方法")
    state = models.SmallIntegerField(choices=STATE_OPTION, null=True, blank=True, default=0,
                                     verbose_name="人脸状态",
                                     help_text="0:正常，1：禁用, 9: 已经删除")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="首次创建的时间",
                                      help_text='指定其在创建数据时将默认写入当前的时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最后更新的时间",
                                      help_text='指定每次数据更新时自动写入当前时间')

    def __str__(self):
        #  如果外键profile存在，则返回self.profile.name，否则返回'unknown'
        if self.profile:
            return f'{self.pk}_{self.profile.name}'
        else:
            return f'{self.pk}_unknown'

    class Meta:
        ordering = ('-created_at',)
        get_latest_by = 'created_at'


class FaceMcs(models.Model):
    id = models.OneToOneField(
        Face,
        related_name='face_mcs',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    file_upload_id = models.IntegerField(default=0, null=True, blank=True, verbose_name="up load file id",
                                         help_text='up load file id')
    file_name = models.CharField(max_length=40, null=True, blank=True, verbose_name="file_name", help_text='file_name')
    file_size = models.IntegerField(default=0, null=True, blank=True, verbose_name="file_size", help_text='file_size')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="updated_at", help_text='updated_at')

    nft_url = models.URLField(
        default='https://calibration-ipfs.filswan.com/ipfs/QmQzPDUheTnFYA7HanxwCLw3QrR7choBvh8pswF4LgxguV', null=True,
        blank=True, verbose_name="NFT 站点", help_text='相当于一个图片源，可以展示图片')
    pin_status = models.CharField(max_length=8, null=True, blank=True, verbose_name="pin_status",
                                  help_text='pin_status')
    payload_cid = models.CharField(max_length=80, null=True, blank=True, verbose_name="payload_cid",
                                   help_text='payload_cid')
    w_cid = models.CharField(max_length=100, null=True, blank=True, verbose_name="w_cid", help_text='w_cid')
    status = models.CharField(max_length=8, null=True, blank=True, verbose_name="status", help_text='status')

    deal_success = models.BooleanField(default=False, blank=True, verbose_name="deal_success", help_text='deal_success')
    is_minted = models.BooleanField(default=False, blank=True, verbose_name="is_minted", help_text='is_minted')
    token_id = models.CharField(max_length=8, null=True, blank=True, verbose_name="token_id", help_text='token_id')
    mint_address = models.CharField(max_length=80, null=True, blank=True, verbose_name="mint_address",
                                    help_text='mint_address')
    nft_tx_hash = models.CharField(max_length=80, null=True, blank=True, verbose_name="nft_tx_hash",
                                   help_text='nft_tx_hash')

    def __str__(self):
        return self.id.name


class FaceLandmarks3D(models.Model):
    face = models.ForeignKey(Face, null=True, on_delete=models.CASCADE, related_name='landmarks3d',
                             verbose_name="所属人脸")
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()


class FaceLandmarks2D(models.Model):
    face = models.ForeignKey(Face, null=True, on_delete=models.CASCADE, related_name='landmarks2d',
                             verbose_name="所属人脸")
    x = models.FloatField()
    y = models.FloatField()


class Kps(models.Model):
    face = models.ForeignKey(Face, null=True, on_delete=models.CASCADE, related_name='kps',
                             verbose_name="所属人脸")
    x = models.FloatField()
    y = models.FloatField()
