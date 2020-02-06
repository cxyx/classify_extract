# coding: utf-8
from __future__ import unicode_literals

import itertools
from sklearn.metrics import precision_recall_fscore_support


class TagsScore(object):

    """
    标签级别的precision, recall, f1
    只支持单字段计算score
    """

    @classmethod
    def score(cls, tags_predict, tags_actual):
        """
        :param tags_predict: list of predict tags
        :param tags_actual: list of actual tags
        tags标签体系：BMESO
        """
        assert isinstance(tags_predict[0], list) and isinstance(tags_actual[0], list)
        
        # dimension 2 -> 1
        tags_predict = list(itertools.chain(*tags_predict))
        tags_actual = list(itertools.chain(*tags_actual))

        assert len(tags_predict) == len(tags_actual)

        # 每个标签的指标
        labels = list(set(tags_predict) | set(tags_actual))
        precisions, recalls, f1s, _ = precision_recall_fscore_support(tags_actual, tags_predict, labels=labels)
        label_scores = {label: dict(zip(('precision', 'recall', 'f1'), zip(precisions, recalls, f1s)[i]))
                        for i, label in enumerate(labels)}
        
        # 除去other标签的micro avg
        other_tag = 'O'
        other_tag_idx = labels.index(other_tag)
        labels_without_other = labels[0:other_tag_idx] + labels[other_tag_idx+1:]
        avg_precision, avg_recall, avg_f1, _ = \
            precision_recall_fscore_support(tags_actual, tags_predict, labels=labels_without_other, average='micro')
        avg_score = {'precision': avg_precision, 'recall': avg_recall, 'f1': avg_f1}
        
        return label_scores, avg_score

