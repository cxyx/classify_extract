# coding:utf-8
# @email: chenyu@datagrand.com
# @author: chenyu

from __future__ import unicode_literals

from word_feature_extractor import WordFeatureExtractor


class WordKeywordsFeatureExtractor(WordFeatureExtractor):
    """
    base特征是字，添加关键词特征
    """

    def __init__(self, content='', tagged_content='', keywords=[], left_word_size=0, right_word_size=0, cut=None):
        assert keywords and (left_word_size >= 0 or right_word_size >= 0)
        self._keywords = keywords
        self._featurevalue_keywords_dict = WordKeywordsFeatureExtractor._create_featurevalue_keywords_dict(keywords)
        self._l_word_size = left_word_size
        self._r_word_size = right_word_size
        WordFeatureExtractor.__init__(self, content=content, tagged_content=tagged_content, cut=cut)

    def add_features(self, base_features):
        word_list = base_features
        features = []
        for index in xrange(len(base_features)):
            feature_value = self._find_keywords_in_context(index, word_list, self._keywords,
                                                           self._l_word_size, self._r_word_size)
            features.append([feature_value])
        return features

    @staticmethod
    def _create_featurevalue_keywords_dict(keywords):
        """
        create featurevalue keywords dict
        :param keywords:类似于[kw1, kw2……]
        :return:类似于{'00':{N, N}, '01':{N, kw2}, '10':{kw1, N}, '11':{kw1, kw2}}
        """
        fv_kws_dict = {}
        combination_count = int(pow(2, len(keywords)))
        for i in range(combination_count):
            feature_value = '0' * (len(keywords) - len(bin(i)[2:])) + bin(i)[2:]
            kws = map(lambda idx: keywords[idx] if feature_value[idx] == '1' else 'N', range(len(feature_value)))
            fv_kws_dict[feature_value] = kws
        return fv_kws_dict

    @staticmethod
    def _find_keywords_in_context(index, word_list, keywords, left_char_size, right_char_size):
        feature_value = ''
        for kw_idx, keyword in enumerate(keywords):
            found = WordKeywordsFeatureExtractor._find_keyword_in_context(index, word_list, keyword, left_char_size,
                                                                          right_char_size)
            feature_value += unicode(found)
        return feature_value

    @staticmethod
    def _find_keyword_in_context(index, word_list, keyword, left_char_size, right_char_size):
        left_border = index - left_char_size if index - left_char_size >= 0 else 0
        right_border = index + right_char_size if index + right_char_size < len(word_list) else len(word_list) - 1
        context = ''.join(word_list[left_border: right_border + 1])
        found = 1 if context.find(keyword) != -1 else 0
        return found
