# coding: utf-8

"""公共"""

import time


def make_order_no(channel):
    """
    功能说明：生成订单编号
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    lbl     2020-07-14         new
    ld      2021-04-14         添加注释
    -------------------------------

    :param channel: int: 支付渠道：1微信，2阿里
    """
    time_str = time.strftime("%Y%m%d%H%M")  # 12位
    micro_second_str = str(int(round(time.time() * 1000000)))  # 微秒字符串  # 16位
    suffix = ''
    if channel == 1:  # 微信
        suffix = 'x_1'
    elif channel == 2:  # 阿里
        suffix = 'x_2'
    order_no = time_str + micro_second_str + suffix
    return order_no
