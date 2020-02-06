# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import abc
import copy
import importlib
import sys
import traceback
from typing import Dict, Text, List

from .. import get_logger
from ..workflow import Workflow
from ..processors.processor_base import ProcessorBase


class BaseEngine(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, conf_module, *args, **kwargs):
        self._conf_module = conf_module
        self._processor_instance_dict = {}
        self._workflow_instance_dict = {}
        self._parse_processors_package()
        self._processor_conf_list, self._workflow_conf_dict = self._parse_conf()
        self._load_processors(*args, **kwargs)
        self._load_workflows(*args, **kwargs)

    def get_workflow(self, workflow_name):
        # type: (Text) -> Workflow
        return self._workflow_instance_dict[workflow_name]

    def _parse_processors_package(self):
        """
        解析processor的路径，在默认配置文件中：
        如果存在absolute_path_to_processor变量，processor将从此路径通，将其加入sys.path,
        如果存在relative_path_to_processor，则将使用相对引用导入processor，并设置self._relative_import_base_package，
        如果以上两个变量都不存在，则默认使用相对引用，默认路径为..app.processors
        """
        if hasattr(self._conf_module, 'absolute_path_to_processor'):
            path_to_processor = self._conf_module.absolute_path_to_processor
            if path_to_processor not in sys.path:
                sys.path.append(path_to_processor)
        else:
            if hasattr(self._conf_module, 'relative_path_to_processor'):
                path_to_processor = self._conf_module.relative_path_to_processor
            else:
                path_to_processor = '..app.processors'
            relative_import_base_module = importlib.import_module(path_to_processor, self._conf_module.__package__)
            self._relative_import_base_package = relative_import_base_module.__name__

    @abc.abstractmethod
    def _parse_conf(self):
        # type: () -> (List, Dict)
        """
        解析参数，返回processor配置的列表和workflow配置的字典
        :return: processor_conf_list, workflow_conf_dict
        """
        pass

    def _load_processors(self, processor_conf_list=None, *args, **kwargs):
        # type: (List, List, Dict) -> None
        if processor_conf_list:
            load_processor_conf_list = processor_conf_list
        else:
            load_processor_conf_list = self._processor_conf_list
        for processor_conf in load_processor_conf_list:
            processor_name = processor_conf['name']
            processor_instance = self._load_processor(copy.deepcopy(processor_conf), *args, **kwargs)
            self._processor_instance_dict[processor_name] = processor_instance
        get_logger().info('load processors success.')

    def _load_processor(self, processor_conf, *args, **kwargs):
        # type: (Dict, List, Dict) -> ProcessorBase
        processor_name = processor_conf['name']
        processor_module = processor_conf['module']
        processor_args = processor_conf['args']
        processor_type = processor_conf.get('type', 'custom')
        processor_comment = processor_conf.get('comment', '')
        get_logger().info('load processor: {}, type: {}'.format(processor_name, processor_type))
        try:
            if '.' in processor_module:
                sub_package, short_module_name = processor_module.rsplit('.', 1)
                module_name = 'processor_' + short_module_name
                full_module_name = sub_package + '.' + module_name
            else:
                module_name = 'processor_' + processor_module
                full_module_name = module_name
            class_name = ''.join([c.capitalize() for c in module_name.split('_')])

            if processor_type == 'custom':
                if hasattr(self, '_relative_import_base_package'):
                    module = importlib.import_module('.' + full_module_name, self._relative_import_base_package)
                else:
                    module = importlib.import_module(full_module_name)
            elif processor_type == 'build_in':
                module = importlib.import_module('.' + full_module_name, 'u_shape_framework.processors')
            else:
                raise RuntimeError('type {} not support'.format(processor_type))

            processor_class = getattr(module, class_name)
            return processor_class(name=processor_name,
                                   processor_args=processor_args,
                                   comment=processor_comment,
                                   *args,
                                   **kwargs)
        except Exception as e:
            get_logger().error('load processor_{} error, exit. error info: {}'.format(processor_name, str(e)))
            get_logger().error(traceback.format_exc())
            exit(-1)

    def _load_workflows(self, workflow_dict=None, *args, **kwargs):
        # type: (Dict, List, Dict) -> None
        if workflow_dict:
            load_workflow_conf_dict = workflow_dict
        else:
            load_workflow_conf_dict = self._workflow_conf_dict
        workflow_name_list = self._topological_sort(load_workflow_conf_dict)

        for workflow_name in workflow_name_list:
            self._workflow_instance_dict[workflow_name] = self._load_workflow(workflow_name,
                                                                              load_workflow_conf_dict[workflow_name],
                                                                              *args, **kwargs)

    def _load_workflow(self, workflow_name, processor_name_list, *args, **kwargs):
        # type: (Text, List, List, Dict) -> Workflow
        return Workflow(workflow_name, processor_name_list, self._processor_instance_dict, self._workflow_instance_dict,
                        *args, **kwargs)

    @staticmethod
    def _topological_sort(workflow_conf):
        graph = {}
        for k, v in workflow_conf.items():
            graph[k] = [n[len('workflow_'):] for n in v if n.startswith('workflow_')]
        in_degrees = dict((u, 0) for u in graph)
        vertex_num = len(in_degrees)
        for u in graph:
            for v in graph[u]:
                in_degrees[v] += 1
        q = [u for u in in_degrees if in_degrees[u] == 0]
        workflow_list = []
        while q:
            u = q.pop(0)
            workflow_list.append(u)
            for v in graph[u]:
                in_degrees[v] -= 1
                if in_degrees[v] == 0:
                    q.append(v)
        if len(workflow_list) != vertex_num:
            raise RuntimeError("there's a circle in workflow conf.")
        workflow_list.reverse()
        return workflow_list

    @abc.abstractmethod
    def destroy(self):
        pass
