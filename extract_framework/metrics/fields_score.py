# coding: utf-8
from __future__ import unicode_literals

import re
import itertools


class FieldsScore(object):

    """
    字段级别的precision, recall, f1
    只支持单字段计算score
    """

    @classmethod
    def score(cls, tags_predict, tags_actual):
        """
        :param tags_predict: list of predict tags
        :param tags_actual: list of actual tags
        tags标签体系：BMESO
        """
        assert isinstance(tags_predict[0], list) and isinstance(tags_actual[0], list)

        # dimension 2 -> 1
        tags_predict = list(itertools.chain(*tags_predict))
        tags_actual = list(itertools.chain(*tags_actual))

        assert len(tags_predict) == len(tags_actual)

        # compute score
        tags_predict = ''.join(map(lambda tag: tag[0], tags_predict))
        tags_actual = ''.join(map(lambda tag: tag[0], tags_actual))
        regex = re.compile('BM*E|S')
        fields_predict = ['{}_{}'.format(m.start(), m.start() + len(m.group())) 
                          for m in regex.finditer(tags_predict)]
        fields_actual = ['{}_{}'.format(m.start(), m.start() + len(m.group()))
                         for m in regex.finditer(tags_actual)]
        predict_num = len(fields_predict)
        actual_num = len(fields_actual)
        correct_num = len(set(fields_predict) & set(fields_actual))
        precision = float(correct_num) / predict_num if predict_num else 0.
        recall = float(correct_num) / actual_num if actual_num else 0.
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.

        return precision, recall, f1

