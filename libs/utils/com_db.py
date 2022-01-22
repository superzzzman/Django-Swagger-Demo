# coding=utf-8
import logging
from django.db import connections, transaction

log = logging.getLogger(__name__)


def exec_sql(sql, db='default'):
    """
    功能说明：   执行SQL
    --------------------------------
    修改人        修改时间        修改原因
    --------------------------------
    lbl        2019-8-12        new
    --------------------------------
    """
    cursor = connections[db].cursor()
    cursor.execute(sql)
    transaction.atomic(using=db)
    cursor.close()
    return True


def fetchone_sql(sql, db='default'):
    """
    功能说明： 查询SQL单条数据
    --------------------------------
    修改人        修改时间        修改原因
    --------------------------------
    lbl        2019-8-12        new
    --------------------------------
    """
    cursor = connections[db].cursor()
    cursor.execute(sql)
    fetchone = cursor.fetchone()
    cursor.close()
    return fetchone


def fetchall_sql(sql, db='default'):
    """
    功能说明：查询SQL多条数据
    --------------------------------
    修改人        修改时间        修改原因
    --------------------------------
    lbl        2019-8-12        new
    --------------------------------
    """
    cursor = connections[db].cursor()
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    cursor.close()
    return fetchall


def fetchall_by_columns(sql, columns, db='default'):
    """
    功能说明：       查询SQL多条数据
    ------------------------------------
    修改人        修改时间        修改原因
    ------------------------------------
    lbl        2019-8-12        new
    ------------------------------------
    参数示例：
    sql = "select username ,password from user"
    columns= ["nickname_username","password"]
    returns:
        [
        {"nickname_username":"王帅","password":"密码"},
        {"nickname_username":"海洋","password":"密码"}
        ]
    """
    cursor = connections[db].cursor()
    cursor.execute(sql)
    object_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    return object_list


def fetchone_to_dict(sql, db='default'):
    """
    功能说明：返回字典对象结果
    --------------------------------
    修改人        修改时间        修改原因
    --------------------------------
    lbl        2019-8-12        new
    --------------------------------
    参数示例：
    sql = "select username ,password from user"
    returns:{"username":"王帅","password":"密码"}
    """
    cursor = connections[db].cursor()
    cursor.execute(sql)
    desc = cursor.description
    # row = dict(zip([col[0] for col in desc], cursor.fetchone() or [""] * len(desc)))
    row = dict(zip([col[0] for col in desc], cursor.fetchone()))
    cursor.close()
    return row


def fetchall_to_dict(sql, db='default'):
    """
    功能说明：返回字典对象结果集
    --------------------------------
    修改人        修改时间        修改原因
    --------------------------------
    lbl        2019-8-12        new
    --------------------------------
    参数示例：
    sql = "select username ,password from user"
    returns:[{"username":"王帅","password":"密码"},{"username":"海洋","password":"密码"}]
    """
    cursor = connections[db].cursor()
    cursor.execute(sql)
    desc = cursor.description
    object_list = [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
    cursor.close()
    return object_list


def call_proc(proname, params=[], db="ketang"):
    """
    功能说明：                调用存储过程
    -----------------------------------------------
    修改人                   修改时间
    -----------------------------------------------
    lbl        2019-8-12        new
    -----------------------------------------------
    proname:    存储过程名字
    params:     输入参数元组或列表
    """
    cursor = connections[db].cursor()
    try:
        cursor.callproc(proname, params)
        #print u'该存储[%s]过程影响的行数：%s' % (proname, cursor.rowcount)
        try:
            transaction.commit_unless_managed(using=db)     # 事务提交
        except Exception as e:
            pass

        data = cursor.fetchall()
        # print '存储过程返回的数据：%s' %data
        cursor.close()
        return data

    except Exception as e:
        log.error('call_proc:%s' % e)
    finally:
        cursor.close()


def sql_filter(sql, max_length=20):
    """
    功能说明：       sql注入过虑
    --------------------------------
    修改人        修改时间        修改原因
    --------------------------------
    lbl        2019-8-12        new
    --------------------------------
    """
    dirty_stuff = ["\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", ">", "+", "%", "$", "(", ")", "%", "@"]
    for stuff in dirty_stuff:
        sql = sql.replace(stuff, "")
    return sql[:max_length]
