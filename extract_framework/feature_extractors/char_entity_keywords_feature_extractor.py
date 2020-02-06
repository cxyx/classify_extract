# coding:utf-8
# @email: chenyu@datagrand.com
# @author: chenyu
from __future__ import unicode_literals

from .char_entity_feature_extractor import CharEntityFeatureExtractor
from .char_keywords_feature_extractor import CharKeywordsFeatureExtractor


class CharEntityKeywordsFeatureExtractor(CharEntityFeatureExtractor, CharKeywordsFeatureExtractor):
    """
    字 + ner 特征抽取
    """

    def __init__(self, content='', tagged_content='', ner=None, keywords=[], left_char_size=0, right_char_size=0):
        CharEntityFeatureExtractor.__init__(self, content=content, tagged_content=tagged_content, ner=ner)
        CharKeywordsFeatureExtractor.__init__(self, content=content, tagged_content=tagged_content, keywords=keywords,
                                              left_char_size=left_char_size, right_char_size=right_char_size)

    def add_features(self, base_features):
        entity_features = CharEntityFeatureExtractor.add_features(self, base_features)
        keywords_features = CharKeywordsFeatureExtractor.add_features(self, base_features)
        features = [entity_features[i] + keywords_features[i] for i in xrange(len(entity_features))]
        return features
