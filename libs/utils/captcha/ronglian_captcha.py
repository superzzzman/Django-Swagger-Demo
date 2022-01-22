# coding: utf-8
# author: zpta
import logging

from ronglian_sms_sdk import SmsSDK

from cms.settings import ACC_ID, ACC_TOKEN, APP_ID

logger = logging.getLogger(__name__)

accId = ACC_ID
accToken = ACC_TOKEN
appId = APP_ID


class RLYunCaptchaHandler(object):
    """
    功能说明：容联云验证码发送
    --------------------------------------------
    修改人        修改时间        修改原因
    --------------------------------------------
    zpt          2021-11-26      new
    --------------------------------------------
    """

    def __init__(self):
        self._accId = ACC_ID
        self._accToken = ACC_TOKEN
        self._appId = APP_ID

    def send_message(self, captcha: str, timeout: int, phone_number: str) -> None:
        """发送验证码

        :param captcha: str: 验证码内容
        :param timeout: int: 过期时间
        :param phone_number: str: 发送电话号码 "178****8888,136****6666"
        :return: None
        """
        sdk = SmsSDK(self._accId, self._accToken, self._appId)
        tid = '1'  # 容联云通讯创建的模板ID
        mobile = phone_number
        keyword_data = (captcha, timeout)  # 模板中替代的关键字信息
        try:
            # resp = sdk.sendMessage(tid, mobile, keyword_data)
            sdk.sendMessage(tid, mobile, keyword_data)
        except Exception as e:
            # print(resp)
            logger.error(e)
        return None


if __name__ == '__main__':
    ronglianyun_captcha = RLYunCaptchaHandler()
    ronglianyun_captcha.send_message(captcha="131468", timeout=10, phone_number="17864733705")
