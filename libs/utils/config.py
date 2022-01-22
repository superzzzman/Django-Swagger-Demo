# coding: utf-8
# author: zpt
from configparser import ConfigParser


class Config(object):
    """配置文件解析"""
    """
    [section_1]
    option = option_value
    [section_2]
    option = option_value
    """
    def __init__(self, file, section=None, encoding="utf-8"):
        self._section = section
        self._cnf = ConfigParser()
        self._cnf.read(file, encoding=encoding)

    def format(self):
        if self._section is None:
            return {key: dict(self._cnf.items(key)) for key in self._cnf.sections()}
        else:
            return dict(self._cnf.items(self._section))

