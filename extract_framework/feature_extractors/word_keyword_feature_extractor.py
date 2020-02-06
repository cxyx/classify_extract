# coding: utf-8
from __future__ import unicode_literals

from word_feature_extractor import WordFeatureExtractor


class WordKeywordFeatureExtractor(WordFeatureExtractor):
    """
    base特征是字，添加关键词特征
    """

    def __init__(self, content='', tagged_content='', cut=None, keyword='', left_word_size=0, right_word_size=0):
        assert keyword != '' and (left_word_size != 0 or right_word_size != 0)
        self._keyword = keyword.decode('utf-8') if type(keyword).__name__ == 'str' else keyword
        self._l_word_size = left_word_size
        self._r_word_size = right_word_size
        super(WordFeatureExtractor, self).__init__(
            content=content, tagged_content=tagged_content, cut=cut)

    def add_features(self, base_features):
        features = []
        for index in xrange(len(base_features)):
            found = self._find_keyword_in_context(index, base_features, self._keyword, self._l_word_size, self._r_word_size)
            features.append([found])
        return features

    @staticmethod
    def _find_keyword_in_context(index, words, keyword, left_char_size, right_char_size):
        left_border = index - left_char_size if index - left_char_size >= 0 else 0
        right_border = index + right_char_size if index + right_char_size < len(words) else len(words) - 1
        context = ''.join(words[left_border: right_border + 1])
        found = 1 if context.find(keyword) != -1 else 0
        return found
