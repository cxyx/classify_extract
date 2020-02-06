# coding: utf-8
from __future__ import unicode_literals

from .feature_extractor_base import FeatureExtractorBase


class CharFeatureExtractor(FeatureExtractorBase):

    """
    字符级别的特征抽取
    """

    def __init__(self, content='', tagged_content=''):
        super(CharFeatureExtractor, self).__init__(content, tagged_content, None)

    def _process_tagged_content(self, tagged_content):
        chars = []
        tags = []
        for term in tagged_content.split('\3'):
            value, tag = term.split('\4')
            if tag == 'O':
                tags += ['O'] * len(value)
            else:
                if len(value) == 1:
                    tags += ['S_%s' % tag]
                else:
                    tags += ['B_%s' % tag] + ['M_%s' % tag] * (len(value) - 2) + \
                            ['E_%s' % tag]
            chars += list(value)
        return chars, tags

    def _process_untagged_content(self, content):
        chars = list(content)
        return chars

    def add_features(self, base_feature):
        pass


