# coding: utf-8
from __future__ import unicode_literals

from .feature_extractor_base import FeatureExtractorBase


class WordFeatureExtractor(FeatureExtractorBase):

    """
    词级别的特征抽取
    """

    def __init__(self, content='', tagged_content='', cut=None):
        assert not cut is None
        super(WordFeatureExtractor, self).__init__(content=content, tagged_content=tagged_content, cut=cut)

    def _process_tagged_content(self, tagged_content):
        words = []
        tags = []
        for term in tagged_content.split('\3'):
            value, tag = term.split('\4')
            values = list(self.cut(value))
            if tag == 'O':
                tags += ['O'] * len(values)
            else:
                if len(values) == 1:
                    tags += ['S_%s' % tag]
                else:
                    tags += ['B_%s' % tag] + ['M_%s' % tag] * (len(values) - 2) + \
                            ['E_%s' % tag]
            words.extend(values)
        return words, tags

    def _process_untagged_content(self, content):
        words = list(self.cut(content))
        return words

    def add_features(self, base_feature):
        pass


