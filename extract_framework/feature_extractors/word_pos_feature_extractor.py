# coding: utf-8
from __future__ import unicode_literals

from .word_feature_extractor import WordFeatureExtractor
from ..utils.norm_pos import norm_pos


class WordPosFeatureExtractor(WordFeatureExtractor):
    """
    词级别+词性 的特征抽取
    """

    def __init__(self, content='', tagged_content='', pos=None):
        assert pos is not None
        super(WordPosFeatureExtractor, self).__init__(
            content=content, tagged_content=tagged_content, cut=pos)

    def _process_tagged_content(self, tagged_content):
        word_pos_list = []
        tags = []
        for term in tagged_content.split('\3'):
            value, tag = term.split('\4')
            values = [[word, norm_pos(pos)] for word, pos in self.cut(value)]
            word_pos_list.extend(values)
            if tag == 'O':
                tags += ['O'] * len(values)
            else:
                if len(values) == 1:
                    tags += ['S_%s' % tag]
                else:
                    tags += ['B_%s' % tag] + ['M_%s' % tag] * (len(values) - 2) + \
                            ['E_%s' % tag]
        return word_pos_list, tags

    def _process_untagged_content(self, content):
        word_pos_list = [[word, norm_pos(pos)] for word, pos in self.cut(content)]
        return word_pos_list

    def add_features(self, base_features):
        features = []
        return features


