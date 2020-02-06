# coding: utf-8
from __future__ import unicode_literals

from char_feature_extractor import CharFeatureExtractor


class CharKeywordFeatureExtractor(CharFeatureExtractor):
    """
    base特征是字，添加关键词特征
    """

    def __init__(self, content='', tagged_content='', keyword='', left_char_size=0, right_char_size=0):
        assert keyword != '' and (left_char_size != 0 or right_char_size != 0)
        self._keyword = keyword.decode('utf-8') if type(keyword).__name__ == 'str' else keyword
        self._l_char_size = left_char_size
        self._r_char_size = right_char_size
        super(CharFeatureExtractor, self).__init__(
            content=content, tagged_content=tagged_content)

    def add_features(self, base_features):
        content = ''.join(base_features)
        features = []
        for index in xrange(len(base_features)):
            found = self._find_keyword_in_context(index, content, self._keyword, self._l_char_size, self._r_char_size)
            features.append([found])
        return features

    @staticmethod
    def _find_keyword_in_context(index, content, keyword, left_char_size, right_char_size):
        left_border = index - left_char_size if index - left_char_size >= 0 else 0
        right_border = index + right_char_size if index + right_char_size < len(content) else len(content) - 1
        context = content[left_border: right_border + 1]
        found = 1 if context.find(keyword) != -1 else 0
        return found
