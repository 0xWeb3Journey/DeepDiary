import os
from datetime import datetime

from django.contrib.auth.models import User, AbstractUser
# Create your models here.
from django.db import models
from django.db.models import Count
# 引入内置信号
from django.db.models.signals import post_save
# 引入信号接收器的装饰器
from django.dispatch import receiver
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFit
from taggit.managers import TaggableManager

SEX_OPTION = (
    (0, "保密"),
    (1, "男"),
    (2, "女"),
)
ROLES_OPTION = (
    ("admin", "Admin"),
    ("editor", "Editor"),
    ("user", "User"),
    ("customer", "Customer"),
    ("employee", "Employee"),
    ("supplier", "Supplier"),
)
STATE_OPTION = (
    (0, "正常"),
    (1, "禁用"),
    (9, "已经删除"),
)
VIP_OPTION = (
    (0, "普通用户"),
    (1, "会员"),
    (2, "高级会员"),
    (3, "黑卡会员"),
)

POSITION_OPTION = (
    (0, "项目经理"),
    (1, "项目"),
    (2, "质量"),
    (3, "商务"),
    (4, "车间"),
    (5, "工艺"),
    (6, "模具"),
    (7, "采购"),
    (8, "物流"),
    (9, "DRE"),
    (10, "SQE"),
    (11, "其它"),
)

# 原始字符串列表
relation_strings = [
    '我', '妻子', '丈夫', '儿子', '女儿', '爸爸', '妈妈', '爷爷', '奶奶', '外公', '外婆',
    '家人', '哥哥', '姐姐', '弟弟', '妹妹', '亲戚', '男朋友', '女朋友', '同事', '朋友',
    '同学', '闺蜜', '客户', '供应商', '合作伙伴', '其他'
]

# 创建字符串到整数的映射
string_to_int_mapping = {s: i for i, s in enumerate(relation_strings)}

# 根据映射生成格式模板
RELATION_OPTION = tuple((i, s) for s, i in string_to_int_mapping.items())


# print(RELATION_OPTION)


def user_directory_path(instance, filename):  # dir struct MEDIA/user/subfolder/file
    sub_folder = "avatar"
    # user_fold = os.path.join(instance.user.username, sub_folder, filename)
    user_fold = os.path.join(instance.username, sub_folder, filename)
    return user_fold


def user_upload_img(instance, filename):  # dir struct MEDIA/user/subfolder/file
    sub_folder = "user_info_img"
    # user_fold = os.path.join(instance.user.username, sub_folder, filename)
    user_fold = os.path.join(sub_folder, filename)
    return user_fold


def user_upload_file(instance, filename):  # dir struct MEDIA/user/subfolder/file
    sub_folder = "user_info_file"
    user_fold = os.path.join(sub_folder, filename)
    return user_fold


# 公司 model
class Company(models.Model):
    employees = models.ManyToManyField('Profile', through='Experience')
    name = models.CharField(max_length=30, blank=True, verbose_name="公司名称", help_text="公司名称")
    addr = models.CharField(max_length=50, blank=True, verbose_name="公司地址", help_text="公司地址")
    desc = models.TextField(blank=True, verbose_name="公司描述", help_text="公司描述")
    tags = TaggableManager(blank=True, verbose_name="公司标签", help_text="可以在这里给公司打上关键字，用','隔开")
    # 数据库更新日期
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="首次创建的时间", help_text="首次创建的时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最后更新的时间", help_text="最后更新的时间")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at',)
        get_latest_by = 'id'


class Address(models.Model):
    company = models.OneToOneField(
        Company,
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


class Profile(AbstractUser):  # 直接继承django默认用户信息
    #  many to many field
    # imgs = models.ManyToManyField('Img', through='Face', related_name='profiles')
    # companies = models.ManyToManyField('Company', through='Experience')
    # events = models.ManyToManyField('Event', through='Participation')  # will be used in diary

    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="真实姓名", help_text="真实姓名")
    full_pinyin = models.CharField(max_length=20, null=True, blank=True, verbose_name="真实姓名全拼",
                                   help_text="真实姓名全拼")
    lazy_pinyin = models.CharField(max_length=20, null=True, blank=True, verbose_name="真实姓名首拼",
                                   help_text="真实姓名首拼")
    tel = models.CharField(max_length=20, blank=True, verbose_name="电话号码", help_text="用户手机号码")
    avatar = models.ImageField(upload_to=user_directory_path,
                               verbose_name="头像",
                               help_text='请上传头像',
                               null=True, blank=True,
                               default='sys_img/logo_lg.png',
                               )
    embedding = models.BinaryField(null=True, blank=True, verbose_name='人脸特征',
                                   help_text='已识别的人脸特征向量')
    relation = TaggableManager(blank=True, verbose_name="relationship",
                               help_text="relationship to the user")
    introduction = models.TextField(max_length=500, blank=True, verbose_name="自我简介", help_text="个人魅力简述")
    # roles = models.SmallIntegerField(choices=ROLES_OPTION, blank=True, default=0, verbose_name="角色",
    #                                  help_text="用户角色/权限")
    roles = models.CharField(max_length=10, choices=ROLES_OPTION, blank=True, default='user', verbose_name="角色",
                             help_text="用户角色/权限")
    gender = models.SmallIntegerField(choices=SEX_OPTION, default=0, blank=True, verbose_name="性别",
                                      help_text="0:保密，1：男, 2： 女")
    birthday = models.DateField(default=datetime.now, blank=True, verbose_name="用户生日", help_text="用户生日")

    # 会员信息
    # user_money = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, verbose_name="余额", help_text="用户生日")
    # accumulate_money = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, verbose_name="累计消费",
    #                                        help_text="累计消费")
    # user_integral = models.IntegerField(default=0, verbose_name="当前积分", help_text="当前积分")
    # visit_count = models.IntegerField(default=0, verbose_name="访问次数", help_text="访问次数")
    # last_time = models.DateTimeField(default=datetime.now, verbose_name="最后一次登入时间", help_text="最后一次登入时间")
    # last_ip = models.GenericIPAddressField(default='192.168.0.1', verbose_name="最后一次访问ip", help_text="最后一次访问ip")
    # country = models.SmallIntegerField(default=0, verbose_name="国家代码", help_text="国家代码")
    # provinces = models.SmallIntegerField(default=0, verbose_name="省代码", help_text="省代码")
    # city = models.SmallIntegerField(default=0, verbose_name="城市代码", help_text="城市代码")
    # district = models.SmallIntegerField(default=0, verbose_name="区县代码", help_text="区县代码")
    # state = models.SmallIntegerField(choices=STATE_OPTION, null=True, blank=True, default=0,
    #                                  verbose_name="账户状态",
    #                                  help_text="0:正常，1：禁用, 9: 已经删除")
    # vip = models.SmallIntegerField(choices=VIP_OPTION, null=True, blank=True, default=0, verbose_name="权限",
    #                                help_text="0: 普通用户, 1: 会员, 2: 高级会员,3:黑卡会员")
    # expired_at = models.DateTimeField(default=datetime.now, verbose_name="会员到期时间", help_text="会员到期时间")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="首次创建的时间", help_text="首次创建的时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最后更新的时间", help_text="最后更新的时间")

    def __str__(self):
        # return f'{self.id}_{self.name}'
        return self.name
        # return f'{self.get_position_display()}_{self.username}'
        # return f'{self.company.name}_{self.position}_{self.name}'

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'avatar': self.avatar,
                'introduction': self.introduction,
                'roles': self.roles,
                }

    @staticmethod
    def get_attr_nums(name):
        # 这里如果不加rst[0]，则返回有2个中括号[[]]
        rst = Profile.objects.annotate(value=Count(name)).values('name', 'value').distinct().order_by(
            '-value'),  # 这里的-是降序，如果不加-则是升序
        return rst[0]

    @staticmethod
    def get_filtered_attr_nums(queryset, name):
        # 这里如果不加rst[0]，则返回有2个中括号[[]]
        rst = queryset.annotate(value=Count(name)).values('name', 'value').distinct().order_by(
            '-value'),  # 这里的-是降序，如果不加-则是升序
        return rst[0]

    class Meta:
        ordering = ('-created_at',)
        get_latest_by = 'id'


# 本模型主要记录朋友之间的关系，备注，描述等信息
class ReContact(models.Model):
    re_from = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, related_name='re_from_relations')
    re_to = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, related_name='re_to_relations')
    relation = models.SmallIntegerField(choices=RELATION_OPTION, blank=True, default=26,
                                        verbose_name="关系", help_text="re_from和re_to的关系")  # 26 mean 其他
    nickname = models.CharField(max_length=20, blank=True, verbose_name="re_from的真实名字",
                                help_text="re_from的真实名字")
    PyInitial = models.CharField(max_length=20, blank=True, verbose_name="re_from的拼音首字母",
                                 help_text="re_from的拼音首字母")
    quanpin = models.CharField(max_length=20, blank=True, verbose_name="re_from的全拼", help_text="re_from的全拼")
    conRemark = models.CharField(max_length=20, blank=True, verbose_name="re_from的备注", help_text="re_from的备注")
    conRemarkPYFull = models.CharField(max_length=20, blank=True, verbose_name="re_from的备注拼音全拼",
                                       help_text="re_from的备注拼音全拼")
    conRemarkPYShort = models.CharField(max_length=20, blank=True, verbose_name="re_from的备注拼音首字母",
                                        help_text="re_from的备注拼音首字母")
    tags = TaggableManager(blank=True, verbose_name="Tags", help_text="给这位联系人打上的标签")
    desc = models.TextField(blank=True, verbose_name="描述", help_text="描述")
    sourceExtInfo = models.CharField(max_length=20, blank=True, verbose_name="来源扩展信息", help_text="来源扩展信息")

    def __str__(self):
        # return f'{self.re_from.name}_{self.re_to.name}_{self.relation}'
        return f'{self.re_from.name}_是_{self.re_to.name}_的_{RELATION_OPTION[self.relation][1]}'

    class Meta:
        ordering = ('re_from',)
        get_latest_by = 'id'
        unique_together = ('re_from', 're_to', 'relation')


class Resource(models.Model):
    profile = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='resources'
    )
    name = models.CharField(blank=True, max_length=30, verbose_name="title of Resource",
                            help_text="title of Resource")
    desc = models.TextField(blank=True, verbose_name="Detail of Resource", help_text="Detail of Resource")
    tags = TaggableManager(blank=True, verbose_name="Tags",
                           help_text="keyword of Detail of Resource，separated by ','")
    # 数据库更新日期
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="首次创建的时间", help_text="首次创建的时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最后更新的时间", help_text="最后更新的时间")

    def __str__(self):
        return self.desc


class Demand(models.Model):
    profile = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='demands'
    )
    name = models.CharField(blank=True, max_length=30, verbose_name="title of demand",
                            help_text="title of demand")
    desc = models.TextField(blank=True, verbose_name="Detail of Demand", help_text="description of Demand")
    tags = TaggableManager(blank=True, verbose_name="Tags",
                           help_text="keyword of Detail of Demand，separated by ','")

    # 数据库更新日期
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="首次创建的时间", help_text="首次创建的时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最后更新的时间", help_text="最后更新的时间")

    def __str__(self):
        return self.desc


class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='experiences')

    position = models.CharField(blank=True, verbose_name="job position",
                                help_text="descript what position you are in charge for", max_length=100)
    start_date = models.DateField(null=True, blank=True, verbose_name="start_date",
                                  help_text="when is this experience started")
    end_date = models.DateField(null=True, blank=True, verbose_name="end_date",
                                help_text="when is this experience end_date")
    name = models.CharField(max_length=30, verbose_name="name", help_text="the title of this experience")
    desc = models.CharField(max_length=300, verbose_name="description", help_text="the detail of this experience")
    achievement = models.CharField(max_length=100, verbose_name="achievement", help_text="fill the achievement you got")
    # 数据库更新日期
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="首次创建的时间", help_text="首次创建的时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最后更新的时间", help_text="最后更新的时间")

    def __str__(self):
        return f"{self.profile.name} worked at {self.company.name}"


class Image(models.Model):
    experience = models.ForeignKey(Experience, null=True, blank=True, on_delete=models.CASCADE, related_name='images',
                                   verbose_name='工作经验', help_text="the images of this experience")
    demand = models.ForeignKey(Demand, null=True, blank=True, on_delete=models.CASCADE, related_name='images',
                               verbose_name='需求', help_text="the images of this demand")
    resource = models.ForeignKey(Resource, null=True, blank=True, on_delete=models.CASCADE, related_name='images',
                                 verbose_name='资源', help_text="the images of this resource")
    src = models.ImageField(upload_to=user_upload_img, verbose_name="图片",
                            help_text='请上传图片',
                            null=True, blank=True,
                            default='sys_img/logo_lg.png')
    thumb = ImageSpecField(source='src',
                           # processors=[ResizeToFill(300, 300)],
                           processors=[ResizeToFit(width=500, height=500)],
                           # processors=[Thumbnail(width=300, height=300, anchor=None, crop=None, upscale=None)],
                           format='JPEG',
                           options={'quality': 80},
                           )


class File(models.Model):
    experience = models.ForeignKey(Experience, null=True, blank=True, on_delete=models.CASCADE, related_name='files',
                                   verbose_name='工作经验', help_text="the files of this experience")
    demand = models.ForeignKey(Demand, null=True, blank=True, on_delete=models.CASCADE, related_name='files',
                               verbose_name='需求', help_text="the files of this demand")
    resource = models.ForeignKey(Resource, null=True, blank=True, on_delete=models.CASCADE, related_name='files',
                                 verbose_name='资源', help_text="the files of this resource")
    file = models.FileField(upload_to=user_upload_file, verbose_name="文件",
                            help_text='请上传文件',
                            null=True, blank=True,
                            default='sys_img/logo_lg.png')
