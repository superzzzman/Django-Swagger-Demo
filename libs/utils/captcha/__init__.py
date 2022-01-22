# coding: utf-8

import string
import random


def simple_number_captcha(k: int = 4) -> str:
    """简单数值验证码"""
    seq = string.digits
    return ''.join(random.choices(seq, k=k))
