# coding: utf-8
from __future__ import unicode_literals


from .char_feature_extractor import CharFeatureExtractor


class CharEntityFeatureExtractor(CharFeatureExtractor):

    """
    字 + ner 特征抽取
    """

    def __init__(self, content='', tagged_content='', ner=None):
        assert ner is not None
        CharFeatureExtractor.__init__(self, content=content, tagged_content=tagged_content)
        self.ner = ner

    def add_features(self, base_feature):
        content = ''.join(base_feature)
        ner_results = list(self.ner(content))
        entities = CharEntityFeatureExtractor.transform_ner_results(content, ner_results)
        features = [[entity] for entity in entities]
        return features

    @staticmethod
    def transform_ner_results(content, ner_results):
        """
        将ner_results转化成entities
        :param content:
        :param ner_results: 
        :return: 
        """
        ner_results.sort(key=lambda term: (term[1], -len(term[0])))
        tmp_set = set()
        entities = ['O'] * len(content)
        for entity, start_idx, end_idx, entity_type in ner_results:
            indexes_set = set(range(start_idx, end_idx))
            if not (tmp_set & indexes_set):
                entities[start_idx:end_idx] = [entity_type] * len(entity)
            tmp_set |= indexes_set
        return entities
