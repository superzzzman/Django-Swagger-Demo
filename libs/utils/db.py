#coding=utf-8
import pymysql
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
config_file = os.path.join(BASE_DIR, 'cms/.env')
DATABASES_CONFIG = ""
try:
    if os.path.isfile(config_file):
        config = open(config_file).read()
        config = json.loads(config)
        DATABASES_CONFIG = config
        HOST = DATABASES_CONFIG['DB_APP_HOST']
        PORT = int(DATABASES_CONFIG['DB_APP_PORT'])
        USER = DATABASES_CONFIG['DB_APP_USER']
        PASSWORD = DATABASES_CONFIG['DB_APP_PASSWORD']
except Exception as ex:
    print('load .env error=%s' % ex)


def conn_ziyuan_basic():
    """author lbl 连接 ziyuan_new 数据库"""
    connect = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        passwd=PASSWORD,
        db='ziyuan_new',
        charset="utf8"
    )
    return connect


def exec_sql(sql, conn=None, close=True):
    """author lbl 执行更新操作SQL"""
    if not sql:
        return None
    if conn is None:
        conn = conn_ziyuan_basic()
    cxn = conn.cursor()
    cxn.execute(sql)
    conn.commit()
    cxn.close()
    if close:
        conn.close()


def fetchall_sql(sql, conn=None, close=True):
    """author lbl 查询sql多条数据"""
    if not sql:
        return None
    if conn is None:
        conn = conn_ziyuan_basic()
    cursor = conn.cursor()
    cursor.execute(sql)
    object_list = cursor.fetchall()
    cursor.close()
    if close:
        conn.close()
    return object_list


def fetchall_to_dict(sql, conn=None, close=True):
    """author lbl 返回字典对象结果"""
    if not sql:
        return None
    if conn is None:
        conn = conn_ziyuan_basic()
    cursor = conn.cursor()
    cursor.execute(sql)
    desc = cursor.description
    object_list = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
    cursor.close()
    if close:
        conn.close()
    return object_list

