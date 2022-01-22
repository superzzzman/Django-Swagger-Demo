# -*-coding:utf-8-*-

"""版本相关"""

import re


class ReVersionList(object):

    __slots__ = ('versions', 'regex_list')

    def __init__(self, versions=()):
        self.versions = list(versions)
        self.regex_list = None
        self._init_regex_list()

    def _init_regex_list(self):
        """编译正则"""
        self.regex_list = [re.compile(version) for version in self.versions]

    def __contains__(self, item):
        """in判断"""
        for regex in self.regex_list:
            if regex.fullmatch(item):
                return True
        return False
