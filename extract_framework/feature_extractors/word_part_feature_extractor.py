# coding:utf-8
# @email: chenyu@datagrand.com
# @author: chenyu

from __future__ import unicode_literals
import math
from word_feature_extractor import WordFeatureExtractor


class WordPartFeatureExtractor(WordFeatureExtractor):
    """
    base特征是词，添加关键词特征
    """

    def __init__(self, content='', tagged_content='', cut=None, part_count=0, occur_part=0):
        '''

        :param content:
        :param tagged_content:
        :param cut:
        :param part_count: 分成多少个part
        :param occur_part: 目标区域在第几个part
        '''
        assert part_count != 0 and occur_part != 0
        self._part_count = part_count
        self._occur_part = occur_part
        super(WordFeatureExtractor, self).__init__(
            content=content, tagged_content=tagged_content, cut=cut)

    def add_features(self, base_features):
        features = []
        for word_idx in xrange(len(base_features)):
            occured = self._occur_in_des_part(word_idx, base_features, self._part_count, self._occur_part)
            features.append([occured])
        return features

    @staticmethod
    def _occur_in_des_part(word_idx, words, part_count, occur_part):
        '''
        判断当前char_idx在正文分成part_count部分以后，是否在目标occur_part
        :param char_idx: 机器计数，从0开始
        :param words:
        :param part_count:
        :param occur_part: 自然计数从1开始，在程序中会-1转换为机器计数，从0开始
        :return:
        '''
        one_part_size = 1.0 * len(words) / part_count
        actual_occ_part = int(math.floor(word_idx / one_part_size))
        occur_part -= 1 #自然计数转换为机器计数
        occured = 1 if actual_occ_part == occur_part else 0

        return occured
