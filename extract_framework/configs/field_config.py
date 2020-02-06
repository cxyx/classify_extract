# coding: utf-8
from __future__ import unicode_literals

import codecs
import json
import os
from collections import OrderedDict
from collections import namedtuple

"""
训练时，每个字段的配置。
加载配置文件，并做合法性检查
"""

CrfConfig = namedtuple('CrfConfig', ['extractor', 'f', 'c', 'template'])
AutoRuleConfig = namedtuple('AutoRuleConfig', ['context_len_before_max', 'context_len_before_min',
                                               'context_len_after'])
DlConfig = namedtuple('DlConfig', ['extractor', 'dl_model_config'])
Extractor = namedtuple('Extractor', ['name', 'kwargs'])


class FieldConfig(object):
    def __init__(self, input_):
        """
        用json结构的文件或字符串初始化
        """
        # assert isinstance(input_, unicode)
        is_path = False
        try:
            if os.path.isfile(input_):
                is_path = True
        except:
            pass
        if is_path:
            content = codecs.open(input_, 'r', 'utf-8').read()
        else:
            content = input_
        self._content = content

        self._config = json.loads(content)
        self._load()

    def _load(self):
        self.field_id = int(self._config['field_id'])
        self.field_name = self._config['field_name']
        self.doctype = int(self._config['doctype'])
        self.data_path = self._config['data_path']
        self.version = self._config['version']
        self.service_names = self._config['services'].keys()
        for service_name in self.service_names:
            if service_name not in ['crf_extract', 'auto_rule_extract', 'dl_extract']:
                raise Exception('service: {} not in {}!'.format(service_name, self.service_names))
            if service_name == 'crf_extract':
                self.crf_config = CrfConfig(
                    extractor=Extractor(name=self._config['services']['crf_extract']['extractor']['name'],
                                        kwargs=self._config['services']['crf_extract']['extractor']['kwargs']),
                    f=self._config['services']['crf_extract']['f'],
                    c=self._config['services']['crf_extract']['c'],
                    template=self._config['services']['crf_extract']['template'])
            if service_name == 'auto_rule_extract':
                self.auto_rule_config = AutoRuleConfig(**self._config['services']['auto_rule_extract'])
            if service_name == 'dl_extract':
                self.dl_config = DlConfig(
                    extractor=Extractor(name=self._config['services']['dl_extract']['extractor']['name'],
                                        kwargs=self._config['services']['dl_extract']['extractor']['kwargs']),
                    dl_model_config=self._config['services']['dl_extract'].get('dl_model_config', {}))
    def dumps(self):
        services = []
        for service_name in self.service_names:
            if service_name == 'crf_extract':
                service = ("crf_extract", {
                    "extractor": {
                        "name": self.crf_config.extractor.name,
                        "kwargs": self.crf_config.extractor.kwargs
                    },
                    "f": self.crf_config.f,
                    "c": self.crf_config.c,
                    "template": self.crf_config.template
                })
            elif service_name == 'auto_rule_extract':
                service = ("auto_rule_extract", {
                    "context_len_before_max": self.auto_rule_config.context_len_before_max,
                    "context_len_before_min": self.auto_rule_config.context_len_before_min,
                    "context_len_after": self.auto_rule_config.context_len_after
                })
            else:
                service = ("dl_extract", {
                    "extractor": {
                        "name": self.dl_config.extractor.name,
                        "kwargs": self.dl_config.extractor.kwargs
                    },
                    "dl_model_config": self.dl_config.dl_model_config
                })
            services.append(service)
        result = OrderedDict([
            ('field_id', self.field_id),
            ('field_name', self.field_name),
            ('doctype', self.doctype),
            ('data_path', self.data_path),
            ('version', self.version),
            ('services', OrderedDict(services))
        ])
        return json.dumps(result, ensure_ascii=False, indent=4, separators=(',', ': '))

    @staticmethod
    def loads(input_):
        return FieldConfig(input_)
