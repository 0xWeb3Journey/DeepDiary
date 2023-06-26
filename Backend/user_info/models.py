import os
from datetime import datetime

from django.contrib.auth.models import User, AbstractUser
# Create your models here.
from django.db import models
# 引入内置信号
from django.db.models.signals import post_save
# 引入信号接收器的装饰器
from django.dispatch import receiver
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


def user_directory_path(instance, filename):  # dir struct MEDIA/user/subfolder/file
    sub_folder = "avatar"
    user_fold = os.path.join(instance.user.username, sub_folder, filename)
    return user_fold


def user_upload_img(instance, filename):  # dir struct MEDIA/user/subfolder/file
    sub_folder = "user_info_img"
    user_fold = os.path.join(instance.user.username, sub_folder, filename)
    return user_fold


def user_upload_file(instance, filename):  # dir struct MEDIA/user/subfolder/file
    sub_folder = "user_info_file"
    user_fold = os.path.join(instance.user.username, sub_folder, filename)
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


class Profile(AbstractUser):  # 直接继承django默认用户信息
    #  many to many field
    # imgs = models.ManyToManyField('Img', through='Face', related_name='profiles')
    # companies = models.ManyToManyField('Company', through='Experience')
    # events = models.ManyToManyField('Event', through='Participation')  # will be used in diary

    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="真实姓名", help_text="真实姓名")
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
        return f'{self.id}_{self.name}'
        # return f'{self.get_position_display()}_{self.username}'
        # return f'{self.company.name}_{self.position}_{self.name}'

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'avatar': self.avatar,
                'introduction': self.introduction,
                'roles': self.roles,
                }

    class Meta:
        ordering = ('-created_at',)
        get_latest_by = 'id'


class SupplyDemand(models.Model):
    profile = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='supplydemand'
    )
    is_demand = models.BooleanField(default=False, blank=True, verbose_name="is_demand",
                                    help_text='False means suppy, True mean demand')
    desc = models.TextField(blank=True, verbose_name="Detail of SupplyDemand", help_text="Detail of SupplyDemand")
    tags = TaggableManager(blank=True, verbose_name="Tags",
                           help_text="keyword of Detail of SupplyDemand，seperated by ','")
    # 数据库更新日期
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="首次创建的时间", help_text="首次创建的时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最后更新的时间", help_text="最后更新的时间")

    def __str__(self):
        return self.desc


class Resource(models.Model):
    profile = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='resources'
    )
    desc = models.TextField(blank=True, verbose_name="Detail of SupplyDemand", help_text="Detail of SupplyDemand")
    tags = TaggableManager(blank=True, verbose_name="Tags",
                           help_text="keyword of Detail of SupplyDemand，seperated by ','")
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
                           help_text="keyword of Detail of SupplyDemand，separated by ','")

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
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='images')
    demand = models.ForeignKey(Demand, on_delete=models.CASCADE, related_name='images')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=user_upload_img, verbose_name="图片",
                              help_text='请上传图片',
                              null=True, blank=True,
                              default='sys_img/logo_lg.png')


class File(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='files')
    demand = models.ForeignKey(Demand, on_delete=models.CASCADE, related_name='files')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=user_upload_file, verbose_name="文件",
                            help_text='请上传文件',
                            null=True, blank=True,
                            default='sys_img/logo_lg.png')
