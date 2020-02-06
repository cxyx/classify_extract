# coding: utf-8
from __future__ import unicode_literals

import re

from base_normalize import BaseNormalize
from ..utils import label_content_util


class TableNormalizer(BaseNormalize):
    """
    归一化表格
    """

    def __init__(self, content, replace_len=None, is_tagged_content=False):
        """
        :param content: 
        :param replace_len: 将表格内容替换成replace_len个\6
        :param is_tagged_content: 是否是带标注的content（\3\4）
        """
        super(TableNormalizer, self).__init__(content)
        self._replace_len = replace_len
        self._is_tagged_content = is_tagged_content

    def _variable_len_normalize(self, equal_len_normed_content):
        """
        对等长归一后的content进行变长归一
        :param equal_len_normed_content: 
        :return: 
        """
        if self._replace_len is not None:
            if self._replace_len == 0:
                regex = re.compile('\6' + '+', re.U)
            else:
                regex = re.compile('\6' * self._replace_len + '+', re.U)
            variable_len_normed_content = regex.sub('\6' * self._replace_len, equal_len_normed_content)
        else:
            variable_len_normed_content = equal_len_normed_content
        self._gen_index_map(equal_len_normed_content, variable_len_normed_content)
        return variable_len_normed_content

    @staticmethod
    def _equal_len_normalize(content):
        """
        表格等长归一化
        :param content: 
        :return: 
        """
        normed_content = content
        regex = re.compile('\[\[[^\5]*\]\]', re.U)
        for match in regex.finditer(content):
            match_value = match.group()
            normed_content = normed_content.replace(match_value, '\6' * len(match_value), 1)
        return normed_content

    def normalize(self):
        if self._is_tagged_content:
            tagged_content = self._content
            content, labels = label_content_util.parse_label_content(tagged_content)
            equal_len_normed_content = self._equal_len_normalize(content)
            labels = [[field, start_idx, end_idx] for field, start_idx, end_idx in labels if
                      equal_len_normed_content[start_idx] != '\6']  # 过滤掉表格标注
            variable_len_normed_content = self._variable_len_normalize(equal_len_normed_content)
            labels = [
                [field, self.get_normed_index_by_raw_index(start_idx), self.get_normed_index_by_raw_index(end_idx)] for
                field, start_idx, end_idx in labels]  # 将labels的索引映射为归一后的索引体系
            variable_len_normed_tagged_content = label_content_util.gen_label_content(variable_len_normed_content,
                                                                                      labels)
            return variable_len_normed_tagged_content
        else:
            equal_len_normed_content = self._equal_len_normalize(self._content)
            variable_len_normed_content = self._variable_len_normalize(equal_len_normed_content)
            return variable_len_normed_content
