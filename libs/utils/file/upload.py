# coding: utf-8

"""文件上传"""

import logging
from collections import deque
from threading import Thread
from typing import List, Optional, Dict, Any
from urllib.parse import urljoin

from django.core.files.uploadedfile import UploadedFile
from django.conf import settings
from oss2 import Auth, Bucket

from libs.utils.common import make_uuid
from libs.utils.file.type import FileCategoryBaseEnum, FileTypeBaseEnum

log = logging.getLogger(__name__)


class UploadThread(Thread):
    """
    功能说明：多线程上传
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    zpta       2021-03-08      new
    -------------------------------
    """

    def __init__(self, file_url: str, file: UploadedFile, num: int, res_list: List[Optional[Dict[str, Any]]],
                 endpoint: str, bucket_name: str, bucket_domain: str, timeout: float,
                 proxy_domain: Optional[str] = None):
        """

        :param file_url: 文件路径
        :param file: 文件
        :param num: 列表下标
        :param res_list: 返回结果列表
        :param endpoint: 端点
        :param bucket_name: bucket
        :param bucket_domain: bucket域名
        :param proxy_domain: 代理域名
        """
        super(UploadThread, self).__init__()
        self.auth = Auth(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET)  # oss服务认证
        self.endpoint = endpoint
        self.bucket_name = bucket_name
        self.bucket_domain = bucket_domain
        self.proxy_domain = proxy_domain
        self.headers = {
            'x-oss-forbid-overwrite': 'true'  # 禁止覆盖同名Object
        }
        self.file_url = file_url
        self.file = file
        self.num = num
        self.res_list = res_list
        self.timeout = timeout

    def run(self):
        try:
            domain = self.proxy_domain or self.bucket_domain
            self.res_list[self.num] = dict(fileAbsUrl=urljoin(domain, self.file_url), status=0)  # 更新url,加上域名
            bucket = Bucket(self.auth, self.endpoint, self.bucket_name, connect_timeout=self.timeout)  # 获取bucket
            response = bucket.put_object(self.file_url, self.file, headers=self.headers)  # 上传
            if response.status == 200:
                self.res_list[self.num]['status'] = 1
        except ValueError as e:
            log.warning(msg='文件上传失败，失败文件："{0}"，失败原因：{1}，报错：{2}'.format(
                self.res_list[self.num]['fileAbsUrl'], '超时', e))
        except Exception as e:
            log.warning(msg='文件上传失败，失败文件："{0}"，报错：{1}'.format(
                self.res_list[self.num]['fileAbsUrl'], e))


class FilesUploadHandler(object):
    """
    功能说明：多线程上传
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    zpt       2021-04-23      new
    -------------------------------
    """

    key_file_list = 'fileAbsUrlDtoList'

    __slots__ = ('_file_list', '_file_category_enum', '_file_type_enum', '_endpoint',
                 '_bucket_name', '_bucket_domain', '_proxy_domain', '_file_url_list')

    def __init__(self, file_list: List[UploadedFile], file_category_enum: FileCategoryBaseEnum,
                 file_type_enum: FileTypeBaseEnum, endpoint: str, bucket_name: str, bucket_domain: str,
                 proxy_domain: Optional[str] = None):
        """

        :param file_list: 文件列表
        :param file_category_enum: 文件分类枚举
        :param file_type_enum: 文件类型枚举
        :param endpoint: 端点
        :param bucket_name: bucket
        :param bucket_domain: bucket域名（访问域名）
        :param proxy_domain: 代理域名
        """
        self._file_list = file_list
        self._file_category_enum = file_category_enum
        self._file_type_enum = file_type_enum
        self._endpoint = endpoint
        self._bucket_name = bucket_name
        self._bucket_domain = bucket_domain
        self._proxy_domain = proxy_domain
        self._file_url_list = []  # 需要返回的上传路径（本地生成，云端oss自动形成路径文件，然后保存文件）
        self._init_file_url()

    def _init_file_url(self):
        """初始化文件地址"""
        for i, file in enumerate(self._file_list, start=0):
            try:
                suffix = str(file).split('.')[-1].lower()  # 提取文件后缀
            except (ValueError, Exception):
                suffix = file.content_type.split('/')[1].lower()  #
            except IndexError as e:
                log.warning(msg='无法获取文件后缀：文件名："{0}"，content_type："{1}"'.format(
                    str(file), file.content_type))
                raise e
            if suffix == 'x-acc':
                suffix = 'aac'

            # 所属/文件类型/uui的数字.后缀
            file_url = '/'.join((
                self._file_category_enum.keyword, '/'.join(self._file_type_enum.path.split('.')), make_uuid()))
            file_url += str(i)  # 防止上传文件列表中文件重复，加数字区别
            file_url += '.' + suffix  # 加后缀（该后缀与传入的文件后缀一致）
            self._file_url_list.append(file_url)

    def upload(self, timeout):
        """上传"""
        if not self._file_list:
            return None
        thread_queue = deque()  # 线程队列
        result_list = [None] * len(self._file_list)  # 生成上传后的结果列表（传几张就有几张的路由地址）
        result = {self.key_file_list: result_list}  # 封装返回结果  {"fileAbsUrlDtoList": []}
        for i, file in enumerate(self._file_list, start=0):
            thread_queue.append(
                UploadThread(file_url=self._file_url_list[i], file=file, num=i, res_list=result_list,
                             endpoint=self._endpoint, bucket_name=self._bucket_name,
                             bucket_domain=self._bucket_domain, proxy_domain=self._proxy_domain, timeout=timeout))
        # 启动线程
        for thread in thread_queue:
            thread.start()
        for thread in thread_queue:
            thread.join()
        return result
