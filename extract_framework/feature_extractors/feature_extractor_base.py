# coding: utf-8
from __future__ import unicode_literals

import abc


class FeatureExtractorBase(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, content='', tagged_content='', cut=None):
        self.content, self.is_tagged = self._load_content(content, tagged_content)
        self.cut = cut

    def _load_content(self, content, tagged_content):
        assert content and not tagged_content or not content and tagged_content, \
                "Please input content or tagged_content!"
        content, is_tagged = (content, False) if content else (tagged_content, True)
        return content, is_tagged    

    @abc.abstractmethod
    def _process_tagged_content(self, tagged_content):
        pass

    @abc.abstractmethod
    def _process_untagged_content(self, content):
        pass

    @abc.abstractmethod
    def add_features(self, base_feature):
        """
        : param base_feature: 字或词特征作为base feature
        增加除了base feature外的其它特征
        """
        pass

    def get_features(self):
        if self.is_tagged:
            base_feature, tags = self._process_tagged_content(self.content)
        else:
            base_feature = self._process_untagged_content(self.content)
        added_features = self.add_features(base_feature)
        if added_features:
            features = map(lambda i: [base_feature[i]] + added_features[i], xrange(len(base_feature)))
        else:
            if base_feature and not isinstance(base_feature[0], list):
                features = map(lambda i: [base_feature[i]], xrange(len(base_feature)))
            else:
                features = base_feature
        return (features, tags) if self.is_tagged else features


