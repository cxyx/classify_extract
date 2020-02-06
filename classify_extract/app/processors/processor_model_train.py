# coding=utf-8
from redis import StrictRedis
from classify_extract.conf import conf

from u_shape_framework.processors.processor_base import ProcessorBase
from classify_extract.app.driver import generate_request_id, logger_offline as logger

import json

class ProcessorModelTrain(ProcessorBase):

    def load(self, args):
        pass

    def up(self, tmp_result, output, request_property):
        pass

    def down(self, tmp_result, output, request_property):
        configs = output['configs']
        try:
            stredis = StrictRedis(conf.REDIS_HOST, conf.REDIS_PORT, conf.REDIS_DB, conf.REDIS_PWD)

            stredis.set('queue:classify:b',json.dumps(output['configs']))  #todo:这里结束,完成redis任务的投放
        except:
            logger.error('redis连接失败')







