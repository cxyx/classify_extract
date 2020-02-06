#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Yang Huiyu
# @Date  : 2019/8/20
# @Email : yanghuiyu@datagrand.com

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import json


class ExtractBean(object):

    def __init__(self, value, start, end, extract_algorithm, score=1.0):
        # type: (unicode, int, int, unicode, float) -> None
        self._value = value
        self._start = start
        self._end = end
        self._score = score
        self._extract_algorithm = extract_algorithm
        self._meta_data_index = None
        self._post_process = None
        self._other = None

    def get_data(self):
        extract_bean = {
            'value': self._value,
            'start': self._start,
            'end': self._end,
            'score': self._score,
            'meta_data_index': self._meta_data_index,
            'post_process': self._post_process,
            'extract_algorithm': self._extract_algorithm,
            'other': self._other
        }
        return extract_bean

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        self._start = start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        self._end = end

    @property
    def post_process(self):
        return self._post_process

    @post_process.setter
    def post_process(self, post_process):
        self._post_process = post_process

    @property
    def meta_data_index(self):
        return self._meta_data_index

    @meta_data_index.setter
    def meta_data_index(self, meta_data_index):
        self._meta_data_index = meta_data_index

    @property
    def extract_algorithm(self):
        return self._extract_algorithm

    @extract_algorithm.setter
    def extract_algorithm(self, extract_algorithm):
        self._extract_algorithm = extract_algorithm

    def __repr__(self):
        return json.dumps(self.get_data(), ensure_ascii=False, indent=4)
