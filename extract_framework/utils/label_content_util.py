# coding: utf-8
from __future__ import unicode_literals

"""
标注数据处理
"""


def parse_label_content(label_content):
    """
    解析标注文本
    :param label_content
    :return: 
    """
    content = ''
    labels = []
    for term in label_content.split('\3'):
        value, tag = term.split('\4')
        content += value
        if tag != 'O':
            field = tag
            start_idx = content.rindex(value)
            end_idx = start_idx + len(value)
            labels.append([field, start_idx, end_idx])
    return content, labels


def gen_label_content(content, labels):
    """
    根据content和labels生成标注content
    :param content: 
    :param labels: 
    :return: 
    """
    labels.sort(key=lambda label: label[1])
    current_index = 0
    tagged_terms = []
    for field, start_idx, end_idx in labels:
        if current_index != start_idx:
            value = content[current_index:start_idx]
            tagged_terms.append('{}\4{}'.format(value, 'O')) if value else None
        value = content[start_idx:end_idx]
        tagged_terms.append('{}\4{}'.format(value, field)) if value else None
        current_index = end_idx
    value = content[current_index:]
    tagged_terms.append('{}\4{}'.format(value, 'O')) if value else None
    return '\3'.join(tagged_terms)
