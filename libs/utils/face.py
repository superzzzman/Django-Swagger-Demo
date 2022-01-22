#!/usr/bin/env python
# coding: utf-8

"""
@author: liuseki
@time: 2021/3/24
@desc: 人脸识别
"""

import logging
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkfacebody.request.v20191230.CompareFaceRequest import CompareFaceRequest
from aliyunsdkfacebody.request.v20191230.DetectLivingFaceRequest import DetectLivingFaceRequest

log = logging.getLogger()


class VerifyHumanFace:
    """
    功能说明：人脸识别
    --------------------------------
    修改人        修改时间       修改原因
    --------------------------------
    ld        2021-03-24        new
    ld        2021-05-18        新增实例变量_exception
    --------------------------------
    """

    __slots__ = ('_access_key_id', '_access_key_secret', '_region_id',
                 '_response', '_exception')

    def __init__(self, access_key_id, access_key_secret, region_id="cn-shanghai"):
        """

        :param access_key_id: str
        :param access_key_secret: str
        :param region_id: str
        """
        self._access_key_id = access_key_id
        self._access_key_secret = access_key_secret
        self._region_id = region_id
        self._response = None  # 结果
        self._exception = None  # 异常


class HumanFaceCompare(VerifyHumanFace):
    """
    功能说明：人脸比对
    --------------------------------
    修改人        修改时间       修改原因
    --------------------------------
    ld        2021-03-24        new
    ld        2021-05-18        新增 exception
    ld        2021-05-19        新增 response_data
    --------------------------------
    """

    @property
    def response_data(self):
        return self._response

    @property
    def exception(self):
        """获取异常"""
        return self._exception

    @property
    def confidence(self):
        """获取可信度

        0-100，越接近100为同一人的比率越高
        :return: float
        """
        if self._response is None:
            return None
        return self._response['Data']['Confidence']

    def compare(self, first_image_url, second_image_url):
        """人脸比对

        文档地址：https://help.aliyun.com/document_detail/151891.html?spm=a2c4g.11186623.6.614.546f1e0f5aQQoY
        :param first_image_url: str: 图片url
        :param second_image_url: str: 图片url
        """
        client = AcsClient(self._access_key_id, self._access_key_secret, self._region_id)
        request = CompareFaceRequest()
        request.set_accept_format('json')
        request.set_ImageURLA(first_image_url)
        request.set_ImageURLB(second_image_url)
        try:
            response = json.loads(client.do_action_with_exception(request))
            log.info('imageA: %s, imageB: %s, response: %s' % (first_image_url, second_image_url, response))
        except ServerException as e:
            self._exception = e
            # response = {
            #     'Data': {'Confidence': 0.0},
            #     'RequestId': e.request_id
            # }
            log.warning('imageA: %s, imageB: %s, exception: %s' % (first_image_url, second_image_url, e))
        else:
            self._response = response
        return None


class DetectLivingFace(VerifyHumanFace):
    """
    功能说明：活体检测——检测是否翻拍
        注意：无法检测是否为人
    --------------------------------
    修改人        修改时间       修改原因
    --------------------------------
    ld        2021-03-24        new
    --------------------------------
    """

    PASS = 'pass'
    REVIEW = 'review'
    BLOCK = 'block'

    @property
    def suggestion(self):
        """获取建议

        pass：图片中的活体对象来自直接拍摄，无需进行其余操作。
        review：图片中的活体对象可能来自翻拍，建议你确认后再进行操作。
        block：图片中的活体对象大概率来自翻拍，建议你执行后续操作。
        """
        if self._response is None:
            return None
        results = self._response['Data']['Elements'][0]['Results']
        return results[0]['Suggestion']

    def single_detect(self, image_url):
        """单人活体检测

        文档地址：https://help.aliyun.com/document_detail/155006.html?spm=a2c4g.11186623.6.609.54d29767tNPHNM
            {
                'Data':
                    {
                        'Elements': [
                            {
                                'ImageURL': 'http://chaoxingqiu.oss-cn-shanghai.aliyuncs.com/demo/image.jpg',
                                'Results': [
                                    {
                                        'Label': 'normal',
                                        'Rate': 42.82,
                                        'Suggestion': 'pass'
                                    }
                                ],
                                'TaskId': 'img6KRej0HCXe05Fj1omqYL31-1u6cda'
                            }
                        ]
                    },
                'RequestId': '8557DB67-F86C-4907-8D7A-D46205D0D922'
            }


        :param image_url: str: 图片地址
        """
        client = AcsClient(self._access_key_id, self._access_key_secret, self._region_id)
        request = DetectLivingFaceRequest()
        request.set_accept_format('json')
        request.set_Taskss([{"ImageURL": image_url}])
        try:
            response = json.loads(client.do_action_with_exception(request))
            log.info('image: %s, response: %s' % (image_url, response))
        except ServerException as e:
            response = {'Data': {'Elements': [{'Results': [{'Suggestion': self.BLOCK}]}]}}
            log.warning('image: %s, exception: %s' % (image_url, e))
        self._response = response
