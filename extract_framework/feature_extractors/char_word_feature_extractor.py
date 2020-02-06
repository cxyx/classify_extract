# coding: utf-8
from __future__ import unicode_literals

from .char_feature_extractor import CharFeatureExtractor


class CharWordFeatureExtractor(CharFeatureExtractor):

    """
    字 + 词 特征抽取
    """

    def __init__(self, content='', tagged_content='', cut=None):
        assert cut is not None
        super(CharWordFeatureExtractor, self).__init__(content=content, tagged_content=tagged_content)
        self.cut = cut

    def add_features(self, base_feature):
        content = ''.join(base_feature)
        features = []
        for word in self.cut(content):
            for _ in word:
                features.append([word])
        return features
