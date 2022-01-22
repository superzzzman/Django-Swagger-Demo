# -*-coding:utf-8-*-

from django.db import connections
from pymysql.cursors import Cursor, DictCursor
from contextlib import contextmanager


class CursorHandler(object):
    """
    功能说明： 封装Cursor
    --------------------------------
    修改人        修改时间        修改原因
    --------------------------------
    ld        2020-08-26        new
    --------------------------------
    """

    __slots__ = ('_cursor', )

    def __init__(self, cursor):
        self._cursor = cursor

    def _execute(self, sql, params=()):
        return self._cursor.execute(sql, params)

    def exec_sql(self, sql, params=(), **kwargs):
        """执行sql返回行数"""
        rows = self._execute(sql, params)
        return rows

    def fetchone(self, sql, params=(), with_rows=False, **kwargs):
        """仅返回一行"""
        rows = self._execute(sql, params)
        result = self._cursor.fetchone()
        if with_rows:
            return rows, result
        return result

    def fetchall(self, sql, params=(), with_rows=False, **kwargs):
        """返回全部"""
        rows = self._execute(sql, params)
        result = self._cursor.fetchall()
        if with_rows:
            return rows, result or []
        return result or []

    def close(self):
        """关闭cursor"""
        self._cursor.close()

    @property
    def cursor(self):
        return self._cursor


class DBSession(object):
    """
    功能说明： 数据库连接session
    --------------------------------
    修改人        修改时间        修改原因
    --------------------------------
    ld        2020-08-26        new
    --------------------------------
    """

    __slots__ = ('conn', 'db')

    def __init__(self):
        self.conn = None
        self.db = 'default'

    def _get_conn(self, db=None):
        conn = connections[self.db if db is None else db]
        conn.ensure_connection()
        conn = conn.connection
        conn.ping()
        return conn

    @staticmethod
    def _get_cursor_class(is_dict):
        return DictCursor if is_dict else Cursor

    def exec_sql(self, sql, params=(), db='default'):
        """
        功能说明：   执行SQL，返回行数
        --------------------------------
        修改人        修改时间        修改原因
        --------------------------------
        ld        2020-08-26        new
        --------------------------------
        参数说明：
        :param sql: str SQL语句
        :param params: tuple/dict SQL值
        :param db: str 库
        :return: int 影响行数，0表示没有改变实际的行
        """
        with self._get_conn(db).cursor() as cur:
            rows = cur.execute(sql, params)
            return rows

    def fetchone(self, sql, params=(), db='default', with_rows=False, is_dict=True):
        """
        功能说明：   执行SQL，返回单行数据
        --------------------------------
        修改人        修改时间        修改原因
        --------------------------------
        ld        2020-08-26        new
        --------------------------------
        参数说明：
        :param sql: str SQL语句
        :param params: tuple/dict SQL值
        :param db: str 库
        :param with_rows: bool 是否返回行数
        :param is_dict: bool 是否返回字典格式结果
        :return: tuple or None
        """
        with self._get_conn(db).cursor(self._get_cursor_class(is_dict)) as cur:
            rows = cur.execute(sql, params)
            result = cur.fetchone()
            if with_rows:
                return rows, result
            return result

    def fetchall(self, sql, params=(), db='default', with_rows=False, is_dict=True):
        """
        功能说明：   执行SQL，返回全部数据
        --------------------------------
        修改人        修改时间        修改原因
        --------------------------------
        ld        2020-08-26        new
        --------------------------------
        :return:
            tuple if is_dict is False
            list if is_dict is True
        """
        with self._get_conn(db).cursor(self._get_cursor_class(is_dict)) as cur:
            rows = cur.execute(sql, params)
            result = cur.fetchall()
            if with_rows:
                return rows, result or []
            return result or []

    def _cursor(self, db='default', is_dict=True):
        """获取cursor"""
        cursor = self._get_conn(db).cursor(self._get_cursor_class(is_dict))
        return CursorHandler(cursor)

    def cursor(self, db='default', is_dict=True):
        """获取cursor
        注意：最后需要手动close
        """
        return self._cursor(db, is_dict)

    @contextmanager
    def context_cursor(self, db='default', is_dict=True):
        """
        功能说明： 获取cursor（上下文协议），减少频繁的cursor.close() 提高性能
        --------------------------------
        修改人        修改时间        修改原因
        --------------------------------
        ld        2020-08-26        new
        --------------------------------
        使用方式：
        with dbs.context_cursor() as cur:
            result1 = cur.fetchall(sql, params=)
            result2 = cur.fetchone(sql, params=)
            ...
        """
        cursor = self._cursor(db, is_dict)
        yield cursor
        cursor.close()


class RawQuerySet(object):
    """
    功能说明：原生SQL转QuerySet，使支持ORM分页
    ------------------------------------
    修改人        修改时间        修改原因
    ------------------------------------
    ld         2020-08-27         new
    ------------------------------------
    """

    __slots__ = ('sql', 'params', 'db', 'dbs', 'is_dict')

    def __init__(self, sql, params=(), db='default', cursor=None, is_dict=True):
        self.sql = sql
        self.params = params
        self.db = db
        self.dbs = cursor if cursor is not None else DBSession()
        self.is_dict = is_dict

    def fetchall(self, sql, is_dict=False):
        is_dict = is_dict if is_dict else self.is_dict
        return self.dbs.fetchall(sql, params=self.params, db=self.db, is_dict=is_dict)

    def count(self):
        """计算总数据条数"""
        sql = 'select count(*) as cnt from ({0}) t'.format(self.sql)
        result = self.fetchall(sql, is_dict=True)
        return result[0]['cnt'] if result else 0

    def __getitem__(self, slc):
        """分页只使用到了切片，此处的slc为slice对象"""
        start, stop = slc.start, slc.stop
        sql = self.sql + f' LIMIT {start}, {stop - start}'
        return self.fetchall(sql)

    def all(self):
        """查询所有数据"""
        return self.fetchall(self.sql)


class EscapeCharacter(object):
    """
    功能说明： 转义字符串方法类
    --------------------------------
    修改人        修改时间        修改原因
    --------------------------------
    ld        2020-08-27        new
    ld        2020-08-31        特殊字符转义
    --------------------------------
    """

    __slots__ = ()

    _escape_table = [chr(s) for s in range(128)]  # 转义表
    _escape_table[ord('%')] = '\\%'
    _escape_table[ord('_')] = '\\_'

    def _escape_string(self, string):
        """特殊字符转义"""
        return string.translate(self._escape_table)

    def right_percent(self, character):
        """右拼接%"""
        return self._escape_string(character) + '%'

    def both_percent(self, character):
        """两边拼接%"""
        return '%' + self._escape_string(character) + '%'


dbs = DBSession()  # db session
ec = EscapeCharacter()  # 转义字符方法
