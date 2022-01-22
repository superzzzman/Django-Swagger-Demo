# coding: utf-8

"""jwt相关"""


import jwt
import time

SALT = '%iai=j+uyd4s0t3qm$3w-w6^b0lf!df%hh-@5f!0&4enc(o7#5'


def jwt_encode(user_id):
    """
    功能说明：jwt编码加密
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld      2021-04-08         new
    --------------------------------
    """
    info = {'user_id': user_id, 'time': time.time()}
    jwt_token = jwt.encode(info, SALT, algorithm='HS256')
    if isinstance(jwt_token, bytes):
        jwt_token = jwt_token.decode('utf-8')
    return jwt_token


def jwt_decode(token):
    """
    功能说明：jwt解码
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld      2021-04-08         new
    --------------------------------
    """
    info = jwt.decode(token.encode("utf-8"), SALT, algorithms=['HS256'])
    return info
