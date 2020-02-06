#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Yang Huiyu
# @Date  : 2018/12/29
from __future__ import unicode_literals

import abc


class BaseNormalize(object):
    """
    对样本进行归一化处理
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, content):
        self._content = content
        self._raw2norm_map = {}
        self._norm2raw_map = {}

    @abc.abstractmethod
    def normalize(self):
        pass

    def get_raw_index_by_normed_index(self, normed_index):
        """
        根据新索引获取原始索引
        """
        return self._norm2raw_map[normed_index]

    def get_normed_index_by_raw_index(self, raw_index):
        """
        根据原始索引找到新索引
        :param raw_index:
        :return:
        """
        return self._raw2norm_map.get(raw_index, -1)

    def get_raw2norm_mapper(self):
        return self._raw2norm_map

    def get_norm2raw_mapper(self):
        return self._norm2raw_map

    def _gen_index_map(self, content, normed_content):
        """
        获取原文与归一化后的坐标映射。
        :param content:
        :param normed_content:
        :return:
        """
        if len(normed_content) == 0:
            return
        # get norm2raw_map
        new_idx = 0
        for raw_idx, raw_char in enumerate(content):
            if normed_content[new_idx] == raw_char:
                self._norm2raw_map[new_idx] = raw_idx
                new_idx += 1
                if new_idx >= len(normed_content):
                    break
        # get raw2norm_map
        self._raw2norm_map = {
            raw_index: norm_index for norm_index, raw_index in self._norm2raw_map.iteritems()
        }