# coding: utf-8
from __future__ import unicode_literals

import os
import codecs

from redis import StrictRedis

from .messages import MessageB
from .messages import MessageC
from .queue_keys import QUEUE_B_FORMATTER
from .queue_keys import QUEUE_C
from .queue_keys import QUEUE_FIELDS_ANALYSIS


class ServiceBase(object):
    def __init__(self, service_name, output_dir, redis_host='127.0.0.1',
                 redis_port=6379, redis_db=0, redis_pwd='', logger=None):
        assert service_name in ('classify_extract','dl_extract', 'crf_extract', 'auto_rule_extract',
                                'sents_search', 'fields_analysis', 'fuzzy_extract', 'table_extract', 'diff_extract')
        self.redis = StrictRedis(redis_host, redis_port, redis_db, redis_pwd)
        self.service_name = service_name
        self.queue_b = QUEUE_B_FORMATTER.format(self.service_name)  #'queue:b:{table_extract}'
        self.logger = logger
        self.output_dir = output_dir

    def start(self):
        if self.logger:
            self.logger.info('service {} starts'.format(self.service_name))
        while True:
            print('我要执行message_bmessage_b')
            message_b = self._read_message()  #根据服务名获取redis里的信息(一直在等在不然不往下执行)
            print('message_b',message_b)
            message_c = self._process(message_b)
            self._write_message(message_c)

    def _process(self, message_b):
        config = message_b.config
        service_name = self.service_name
        status = 'OK'
        msg = 'OK'
        # create version dir
        version_path = '{}/{}'.format(self.output_dir, config.version)
        if not os.path.isdir(version_path):
            os.system('mkdir {}'.format(version_path))
        # delete old status file if exists
        error_file = '{}/{}/{}.{}'.format(self.output_dir, config.version, config.field_id, 'ERROR')
        ok_file = '{}/{}/{}.{}'.format(self.output_dir, config.version, config.field_id, 'OK')
        if os.path.isfile(error_file):
            os.system('rm {}'.format(error_file))
        if os.path.isfile(ok_file):
            os.system('rm {}'.format(ok_file))
        # run
        try:
            self._run(config)
        except Exception as e:
            if self.logger:
                self.logger.exception(e)
            status = 'ERROR'
            msg = str(e)
        # write status to file
        # codecs.open('{}/{}/{}.{}'.format(self.output_dir, config.version, config.field_id, status), 'w').write(msg)
        message_c = MessageC(config.version, service_name, config.field_id, status, msg)
        return message_c

    def _run(self, config):
        pass  # TODO

    def _read_message(self):
        # read message B from queue B
        return MessageB.load(self.redis.brpop(self.queue_b)[1])   #'queue:b:table_extract'

    def _write_message(self, message_c):
        # write message C to queue C
        if self.service_name == 'fields_analysis':
            self.redis.lpush(QUEUE_FIELDS_ANALYSIS, str(message_c))
        else:
            self.redis.lpush(QUEUE_C, str(message_c))
