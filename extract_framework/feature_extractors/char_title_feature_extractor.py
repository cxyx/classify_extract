# coding: utf-8
from __future__ import unicode_literals

import re

from char_feature_extractor import CharFeatureExtractor


class CharTitleFeatureExtractor(CharFeatureExtractor):
    """
    base特征是字，添加标题特征
    """

    def __init__(self, content='', tagged_content='', title_level='', title_name=''):
        assert title_level != '' and title_name != ''
        self._title_level = title_level
        self._title_name = title_name
        super(CharFeatureExtractor, self).__init__(
            content=content, tagged_content=tagged_content)

    def add_features(self, base_features):
        content = ''.join(base_features)
        features = []
        for index in xrange(len(base_features)):
            found = self._find_belonging_title(index, content, self._title_level, self._title_name)
            features.append([found])
        return features

    @staticmethod
    def _find_belonging_title(index, content, title_level, title_name):
        context = content[0: index]
        regex_str = '{0}[ \t]*{1}((?!{0}).)*?$'.format(title_level, title_name)
        match = re.search(regex_str, context)
        found = 1 if match else 0
        return found
