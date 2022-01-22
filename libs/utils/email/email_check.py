# coding:utf-8

import re


def validateEmail(email):
    if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
        # if re.match("/^\w+@[a-z0-9]+\.[a-z]{2,4}$/", email) != None:
        print("ok")
        return 'ok'
    else:
        print("fail")
        return 'fail'


# validateEmail('01550@cto.net.cn')
validateEmail("zpta_super@163.com")
validateEmail("1260844462@qq.com")
