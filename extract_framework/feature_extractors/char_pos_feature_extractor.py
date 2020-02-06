# coding: utf-8
from __future__ import unicode_literals

from .char_feature_extractor import CharFeatureExtractor
from ..utils.norm_pos import norm_pos


class CharPosFeatureExtractor(CharFeatureExtractor):
    """
    字级别添加词性
    """

    def __init__(self, content='', tagged_content='', pos=None):
        assert pos is not None
        self._pos = pos
        super(CharFeatureExtractor, self).__init__(
            content=content, tagged_content=tagged_content)

    def add_features(self, base_features):
        content = ''.join(base_features)
        features = []
        for word, pos in self._pos(content):
            pos = norm_pos(pos)
            if len(word) == 1:
                features.append(['S_{}'.format(pos)])
            else:
                cut_result = 'B' + 'M' * (len(word) - 2) + 'E'
                for c in cut_result:
                    features.append(['{}_{}'.format(c, pos)])
        return features


