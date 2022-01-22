# coding: utf-8

"""验证码缓存"""

from typing import Union

from .type import CaptchaTypeBaseEnum

__all__ = (
    'get_captcha_cache_key',
)


_CACHE_KEYWORD_SEP: str = ':'
_CACHE_PREFIX: str = 'captcha'


def get_captcha_cache_key(keyword: str, unique_id: Union[str, int]) -> str:
    """获取验证码缓存keyword

    :param keyword: 关键字
    :param unique_id: 唯一id
    :return: str
    """
    """获取缓存的key"""
    return _CACHE_KEYWORD_SEP.join((_CACHE_PREFIX, keyword, unique_id))
