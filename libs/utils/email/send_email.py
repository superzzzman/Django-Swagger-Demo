# coding: utf-8
# author: zpt
import logging
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from cms.settings import EMAIL_HOST, EMAIL_USER, EMAIL_PASS, EMAIL_SENDER

logger = logging.getLogger(__name__)


class EmailHandler(object):
    """
    功能说明：邮件相关操作类
    --------------------------------
    修改人       修改时间       修改原因
    --------------------------------
    zpt       2021-11-25       new
    --------------------------------
    """

    def __init__(self):
        # 163邮箱服务器地址
        self._mail_host = EMAIL_HOST
        # 163用户名
        self._mail_user = EMAIL_USER
        # 密码(部分邮箱为授权码)
        self._mail_pass = EMAIL_PASS
        # 邮件发送方邮箱地址
        self._sender = EMAIL_SENDER

    def send_email(self, receivers: list, content: str) -> None:
        """用于发邮件验证码

        :param receivers: list: 接收消息人（只能是列表，且只能有一个元素）
        :param content:
        :return:
        """
        # 设置服务器所需信息
        # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        receivers = receivers
        content: str = f"感谢您加入完美账本，您的验证码为：{content}，别告诉别人哦！"
        title: str = "Bill"

        # 设置email信息
        # 邮件内容设置
        message = MIMEText(content, 'plain', 'utf-8')
        # 邮件主题
        message['Subject'] = title
        # 发送方信息
        message['From'] = self._sender
        # 接受方信息
        message['To'] = receivers[0]

        # 登录并发送邮件
        try:
            smtp_obj = smtplib.SMTP()
            # 连接到服务器
            smtp_obj.connect(self._mail_host, 25)
            # 登录到服务器
            smtp_obj.login(self._mail_user, self._mail_pass)
            # 发送
            smtp_obj.sendmail(
                self._sender, receivers, message.as_string())
            # 退出
            smtp_obj.quit()
            # print('success')
        except smtplib.SMTPException as e:
            # print('error', e)  # 打印错误
            logger.error(e)
        return None


if __name__ == '__main__':
    email = EmailHandler()
    email.send_email(["zpta_super@163.com"], content="898989")
