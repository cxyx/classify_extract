# coding: utf-8
from __future__ import unicode_literals

import re
import json
import codecs
import random
import sys


class DataAugmentation(object):

    def __init__(self, input_file_path, output_file_path):
        self._input_file_path = input_file_path
        self._output_file_path = output_file_path

    @staticmethod
    def _get_context_values_from_article(tagged_content, field_id):
        """
        根据单篇标注好的\3\4文本生成 上下文、values
        """
        regex = re.compile('\3(.*?)\4' + unicode(field_id) + '\3')
        values = []
        context = tagged_content
        for match in regex.finditer(tagged_content):
            value = match.group(1)
            context = context.replace(match.group(), '\3*****\4' + unicode(field_id) + '\3')
            values.append(value)
        return context, values

    @staticmethod
    def _get_all_context_values(data_file):
        """
        获得单个字段的所有 上下文、values
        data_file: 某个字段的所有标注文档
        """
        field_id = data_file.split('_')[0]
        contexts = set()
        all_values = set()
        for line in codecs.open(data_file, 'r', 'utf-8'):
            tagged_content = line.strip()
            if tagged_content:
                context, values = DataAugmentation._get_context_values_from_article(tagged_content, 
                                                                                    field_id)
                all_values |= set(values)
                contexts.add(context)
        return list(contexts), list(all_values)

    def augment(self, copy_num):
        contexts, all_values = DataAugmentation._get_all_context_values(self._input_file_path)
        out = codecs.open(self._output_file_path, 'w', 'utf-8')
        for _ in range(copy_num):
            context = random.choice(contexts)
            value = random.choice(all_values)
            content = context.replace('*****', value)
            out.write(content + '\n')


