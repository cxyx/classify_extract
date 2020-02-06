# coding=utf-8
# email:  xgao85@gmail.com
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .procession import Procession
from . import get_logger
from typing import Dict


class Workflow(object):

    def __init__(self,
                 workflow_name,
                 processor_name_list,
                 processor_instance_dict,
                 loaded_workflow_list=None,
                 user_manager=None):
        """
        Workflow是一个具体任务的工作流，包含一系列processor实例的引用，可以完成复杂的业务流程，是无状态的
        :param workflow_name: workflow的名字，是workflow的唯一标志符
        :param processor_name_list: 该参数决定了Processor实例的组合
        :param processor_instance_dict: 存有engine中所有processor实例的引用
        :param loaded_workflow_list: 已加载的workflow列表，用于实现workflow嵌套
        """

        if loaded_workflow_list is None:
            loaded_workflow_list = []
        get_logger().info('init workflow {}'.format(workflow_name))
        self.name = workflow_name
        self._user_manager = user_manager
        self._loaded_workflow_list = loaded_workflow_list
        self._processors = []
        self._load_processors(processor_name_list, processor_instance_dict)

    def _load_processors(self, processor_name_list, processor_instance_dict):
        for processor_name in processor_name_list:
            if processor_name.startswith('workflow_'):
                workflow_name = processor_name[len('workflow_'):]
                workflow = self._loaded_workflow_list[workflow_name]
                self._processors.extend(workflow.processors)
            else:
                processor = processor_instance_dict[processor_name]
                self._processors.append(processor)

    def _create_procession(self, request_property):
        # type: (Dict) -> Procession
        """
        生成procession
        :param request_property: 该参数为procession的属性，如request id, app id等
        :return:
        """
        return Procession(self._processors, request_property)

    def run(self, request_property, tmp_result=None):
        # type: (Dict, Dict) -> Dict
        if tmp_result is None:
            tmp_result = {}
        if self._user_manager:
            user_args = {}
            for processor in self._processors:
                processor_name = processor.name
                system_processor_args = processor.args
                user_id = request_property['user_id']
                user_processor_args = self._user_manager.get_user_u_shape_framework_conf(
                    user_id, processor_name, system_processor_args)
                user_args[processor_name] = user_processor_args
            request_property['user_args'] = user_args
        procession = self._create_procession(request_property)
        output = procession.run(tmp_result)
        return output

    @property
    def processors(self):
        return self._processors
