from celery import shared_task

from user_info.models import Profile, Company, Assert
from pypinyin import lazy_pinyin, pinyin, Style

from utilities.common import trace_function
import logging

logger = logging.getLogger(__name__)


def get_pinyin(name):
    if name is None:
        return None, None
    # full_pinyin = ''.join([item[0] for item in pinyin(name, style=Style.NORMAL)])
    full_pinyin = ''.join(lazy_pinyin(name))
    lazy_pinyin_str = ''.join(lazy_pinyin(name, style=Style.FIRST_LETTER))
    return full_pinyin, lazy_pinyin_str


class ProfileProcess:
    def __init__(self):
        """
        初始化函数，对profile 模型做一些处理，比如生成拼音等
        """
        print('INFO: ProfileProces init')

    def __is_need_process__(self, instance=None, force=False, field=None):
        """
        判断是否需要处理
        :param instance: 实例对象
        :param force: 是否强制处理
        :param field: 字段名
        :return: process: 是否需要处理
        """
        process = False
        # 1. 判断instance 是否是Profile 类型的实例
        if not isinstance(instance, Profile):
            print(f'--------------------{instance.id} :instance is not Profile---------------------------')
            return process

        if field is not None and hasattr(instance, field):
            value = getattr(instance, field)
            if force:
                print(f'INFO: force stat is {force}')
                process = True
            if not value:
                print(f'INFO: {field} is {value}')
                process = True
        else:
            print(f'INFO: {field} is not exist')
        return process

    # @shared_task
    def get_pinyin(self, instance=None, force=False):
        # 1. 判断是否需要处理
        field = 'full_pinyin'
        process = self.__is_need_process__(instance, force, field)
        if not process:
            return

        instance.full_pinyin, instance.lazy_pinyin = get_pinyin(instance.name)
        instance.save()

        print(f'--------------------{instance.id} :process successes---------------------------')

    @staticmethod
    @trace_function
    def get_asserts(instance=None, force=False):
        if not instance:
            return
        asserts, created = Assert.objects.get_or_create(profile=instance)  # bind the one to one field image info
        asserts.face_cnt = instance.faces.count()
        asserts.img_cnt = instance.imgs.count()
        asserts.friend_cnt = instance.re_from_relations.count() + instance.re_to_relations.count()
        asserts.save()

        print(f'--------------------{instance.id} :process successes---------------------------')

    # ----------------------process for single profile for several functions----------------------
    @shared_task
    def get_profile(self, instance=None, func_list=None, force=False):
        """
        :param instance: the instance of the image
        :param func_list: the list of the function
        :param force: if force is True, then the function will be executed
        the function list could be as follows:
        func_list = ['get_pinyin']
        get_pinyin(self, instance=None, force=False)
        :return:
        """
        print(
            f'-------------INFO: start loop the  funcs, dealing with profile --->{instance.id}, func_list is {func_list}---------------')
        if func_list is None:
            func_list = ['get_pinyin', 'get_asserts']
        # 2. loop the function list
        for func_name in func_list:
            print(
                f'-------------INFO: This is func: {func_name} , dealing with profile --->{instance.id}---------------')
            func = getattr(self, func_name, None)
            if func is None:
                print(
                    f'-------------INFO: there is no func: {func_name} , dealing with profile --->{instance.id}---------------')
                continue
            func(instance=instance, force=force)

    #  ----------------------process for all the profiles for several functions----------------------
    @shared_task
    def get_all_profile(self, func_list=None, force=False):
        """
        :param func_list: the list of the function
        :param force: if force is True, then the function will be executed
        the function list could be as follows:
        func_list = ['get_pinyin']
        get_pinyin(self, instance=None, force=False)

        :return:
        """
        if func_list is None:
            return
        # 1. get all the profiles
        profiles = Profile.objects.all()
        # 2. Go through each profile
        for (profile_idx, profile) in enumerate(profiles):
            print(f'--------------------INFO: This is profile{profile_idx}: {profile.id} ---------------------')

            self.get_profile(self, instance=profile, func_list=func_list, force=force)


class CompanyProcess:
    def __init__(self):
        """
        初始化函数，对Company 模型做一些处理，比如生成拼音等
        """
        print('INFO: CompanyProces init')

    def __is_need_process__(self, instance=None, force=False, field=None):
        """
        判断是否需要处理
        :param instance: 实例对象
        :param force: 是否强制处理
        :param field: 字段名
        :return: process: 是否需要处理
        """
        process = False
        # 1. 判断instance 是否是Profile 类型的实例
        if not isinstance(instance, Company):
            print(f'--------------------{instance.id} :instance is not Company---------------------------')
            return process

        if field is not None and hasattr(instance, field):
            value = getattr(instance, field)
            if force:
                print(f'INFO: force stat is {force}')
                process = True
            if not value:
                print(f'INFO: {field} is {value}')
                process = True
        return process

    # @shared_task
    def get_pinyin(self, instance=None, force=False):
        # 1. 判断是否需要处理
        field = 'name_PyFull'
        process = self.__is_need_process__(instance, force, field)
        if not process:
            return

        instance.name_PyFull, instance.name_PyInitial = get_pinyin(instance.name)
        instance.save()

        print(f'--------------------{instance.id} :process successes---------------------------')

    # ----------------------process for single profile for several functions----------------------
    @shared_task
    def get_company(self, instance=None, func_list=None, force=False):
        """
        :param instance: the instance of the image
        :param func_list: the list of the function
        :param force: if force is True, then the function will be executed
        the function list could be as follows:
        func_list = ['get_pinyin']
        get_pinyin(self, instance=None, force=False)
        :return:
        """
        print(
            f'-------------INFO: start loop the  funcs, dealing with profile --->{instance.id}, func_list is {func_list}---------------')
        if func_list is None:
            func_list = ['get_pinyin']
        # 2. loop the function list
        for func_name in func_list:
            print(
                f'-------------INFO: This is func: {func_name} , dealing with profile --->{instance.id}---------------')
            func = getattr(self, func_name, None)
            if func is None:
                print(
                    f'-------------INFO: there is no func: {func_name} , dealing with profile --->{instance.id}---------------')
                continue
            func(instance=instance, force=force)

    #  ----------------------process for all the profiles for several functions----------------------
    @shared_task
    def get_all_company(self, func_list=None, force=False):
        """
        :param func_list: the list of the function
        :param force: if force is True, then the function will be executed
        the function list could be as follows:
        func_list = ['get_pinyin']
        get_pinyin(self, instance=None, force=False)

        :return:
        """
        if func_list is None:
            return
        # 1. get all the profiles
        companies = Company.objects.all()
        # 2. Go through each profile
        for (company_idx, company) in enumerate(companies):
            print(f'--------------------INFO: This is profile{company_idx}: {company.id} ---------------------')

            self.get_company(self, instance=company, func_list=func_list, force=force)
