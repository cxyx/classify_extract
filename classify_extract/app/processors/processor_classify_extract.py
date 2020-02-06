# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import traceback
import sys

from ..common.extract_tools import start_extract
from u_shape_framework.processors.processor_base import ProcessorBase
from ..driver import logger_offline as logger


class ProcessorClassifyExtract(ProcessorBase):
    '''
    func:将线上的配置文件与本地合并,线上优先
    后期版本可能增加更新部分配置,较多代码,所以单独processor,目前更新所有的
    '''

    def load(self, args):
        self._args = args

    def up(self, tmp_result, output, request_property):
        pass

    def down(self, tmp_result, output, request_property):
        print('ProcessorClassifyExtract')
        model_dir = tmp_result.get('config_model_dir')
        # model_dir = request_property.get('output_dir')
        output['status'] = 'ERROR'
        try:
            opontions, prerequisite, requirement = tmp_result.get('opontions'), tmp_result.get(
                'prerequisite'), tmp_result.get('requirement')
            print('opontions, prerequisite, requirement',opontions, prerequisite, requirement)

        except Exception as e:
            logger.error('获取part信息失败')

        try:
            return_items = start_extract(opontions, prerequisite, requirement, model_dir)
            print('returnreturn_items_items',return_items)
            logger.info('抽取结果为:{}......'.format(str(return_items)[0:100]))
            print('aaaaaaaaaaaaa')
            output['status'] = 'OK'
            output['return_items'] = return_items
            output['msg'] = ''
            logger.info('抽取成功抽取成功')

        except Exception as e:
            output['return_items'] = {}
            logger.error('抽取失败')
            output['status'] = 'ERROR'
            output['msg'] = ''
