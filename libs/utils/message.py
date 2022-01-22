# coding=utf-8
import uuid
import time
import random
import string
import hashlib
import datetime
import json
from libs.utils.common import make_uuid
from libs.models.models import SysMsg, MsgNumber
from django.db.models import F
from apps.rongcloud.rongcloud import RongCloud
from django.conf import settings
RC = RongCloud(settings.RONGYUN_KEY, settings.RONGYUN_SECRET)


def send_sys_msg(params):
    """
    功能说明：发送系统消息
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    lbl      2020/06/02         new
    """
    first_id = params.get("first_id", "")  # 第一个跳转的Id
    first_name = params.get("first_name", "")  # 第一个名字
    first_to = params.get("first_to", 1)  # 1用户 2商家 3圈子 4商品 -1不跳转
    second_id = params.get("second_id", "")  # 第二个跳转的Id
    second_name = params.get("second_name", "")  # 第二个名字
    second_to = params.get("second_to", 1)  # 1用户 2商家 3圈子 4商品 -1不跳转
    thirdly_id = params.get("thirdly_id", "")  # 第二个跳转的Id
    thirdly_name = params.get("thirdly_name", "")  # 第二个名字
    thirdly_to = params.get("thirdly_to", 1)  # 1用户 2商家 3圈子 4商品 -1不跳转
    action_name = params.get("action_name", "")  # 点击按钮
    title_name = params.get("title_name", "")  # 标题名称
    api = params.get("api", "")  # 条状api接口
    button_status = params.get("button_status", 0)  # 是否有点击  0为不可以 1可以
    type = params.get("type", -1)  # 类型 0跳转图片 1跳转接口 2跳转钱包 -1 不跳转
    skip_image = params.get("skip_image", "")  # 跳转图片的地址
    user_id = params.get("user_id", "")  # 用户Id
    content = params.get("content", "")  # 内容
    object_id = params.get("object_id", "")  # 需要跳转地方的Id
    status = params.get("status", 1)  # 状态
    data = {"skipImage": skip_image, "type": type}
    if first_id:
        data = {
            "type": type,
            "firstId": first_id,
            "firstName": first_name,
            "firstTo": first_to,
            "api": api,
            "skipImage": skip_image
        }
    if second_id and first_id:
        data = {
            "type": type,
            "secondId": second_id,
            "secondName": second_name,
            "secondTo": second_to,
            "firstId": first_id,
            "firstName": first_name,
            "firstTo": first_to,
            "api": api,
            "skipImage": skip_image,
        }
    if thirdly_id and second_id and first_id:
        data = {
            "thirdlyId": thirdly_id,
            "thirdlyName": thirdly_name,
            "thirdlyTo": thirdly_to,
            "type": type,
            "secondId": second_id,
            "secondName": second_name,
            "secondTo": second_to,
            "firstId": first_id,
            "firstName": first_name,
            "firstTo": first_to,
            "api": api,
            "skipImage": skip_image,
        }
    create_time = datetime.datetime.now()
    SysMsg.objects.create(title_name=title_name, sys_msg_id=make_uuid(), user_id=user_id, data=json.dumps(data),
                          content=content, action_name=action_name, button_status=button_status, create_time=create_time,
                          update_time=create_time, object_id=object_id, type=status)
    query_set = MsgNumber.objects.filter(user_id=user_id)
    if query_set:
        query_set.update(user_id=user_id, sum_unread=F("sum_unread") + 1,
                         sys_count=F("sys_count") + 1, status=1, update_time=create_time)
    else:
        query_set.create(msg_number_id=make_uuid(), user_id=user_id, sum_unread=1,
                         sys_count=1, status=1, create_time=create_time, update_time=create_time)


def push_sys_msg(to_user_ids, content):
    """
    功能说明：推送消息
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    lbl      2020/06/17         new
    --------------------------------
    说明：使用系统通知账号发送单聊消息并在通知栏显示
    """
    from_user_id = "6d8832bdb2d93a5cb47e6fbb"  # 系统通知账号
    object_name = "RC:TxtMsg"
    msg_content = {"content": content, "extra": ""}
    push_content = content
    if len(to_user_ids) > 1000:
        RC.get_message().get_private().send(from_user_id, to_user_ids[:1000], object_name, msg_content, push_content, push_content)
        return push_sys_msg(to_user_ids[1000:], content)
    else:
        RC.get_message().get_private().send(from_user_id, to_user_ids, object_name, msg_content, push_content, push_content)
        return True

