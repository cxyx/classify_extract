# coding: utf-8
from __future__ import unicode_literals

import abc
import json
import demjson
from ..configs.field_config import FieldConfig


class MessageBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __str__(self):
        pass

    def dump(self):
        return self.__str__()

    @abc.abstractmethod
    def load(cls, string):
        pass


class MessageA(MessageBase):

    def __init__(self, version, doctype, tasks, configs):
        assert isinstance(version, unicode) and isinstance(doctype, unicode) and isinstance(tasks, list)
        for config in configs:
            assert config.__class__ == FieldConfig
        self.version = version
        self.doctype = doctype
        self.tasks = tasks
        self.configs = configs

    def __str__(self):
        result = {'version': self.version, 'doctype': self.doctype, 'tasks': self.tasks, 
                  'configs': [c.dumps() for c in self.configs]}
        return json.dumps(result)

    @classmethod
    def load(cls, string):
        result = json.loads(string)
        return MessageA(result['version'], result['doctype'], result['tasks'],
                        [FieldConfig.loads(c) for c in result['configs']])


class MessageB(MessageBase):

    def __init__(self, config):
        assert isinstance(config, FieldConfig)  #是否为实例对象
        self.config = config

    def __str__(self):
        result = {'config': self.config.dumps()}

        return json.dumps(result)

    @classmethod
    def load(cls, string):
        result = json.loads(string)
        return MessageB(FieldConfig.loads(result['config']))


class MessageC(MessageBase):

    def __init__(self, version, service_name, field, status, msg=''):
        # assert isinstance(version, str) and isinstance(service_name, str) \
        #         and isinstance(field, int) and status in ('OK', 'ERROR') and isinstance(msg, str)
        self.version = version
        self.service_name = service_name
        self.field = field
        self.status = status
        self.msg = msg

    def __str__(self):
        result = {'version': self.version, 'service_name': self.service_name, 'field': self.field, \
                  'status': self.status, 'msg': self.msg}
        return json.dumps(result)

    @classmethod
    def load(cls, string):
        result = json.loads(string)
        return MessageC(result['version'], result['service_name'], result['field'], result['status'], result['msg'])


