# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import copy
from typing import Text, Any
from ..user_manager import UserManager
from .base_engine import BaseEngine


class MultiUserEngine(BaseEngine):

    def __init__(self, conf_module, user_management_path):
        # type: (Any, Text) -> None
        conf_module_name = conf_module.__name__
        if '.' in conf_module_name:
            u_shape_framework_conf_name = conf_module_name.rsplit('.', 1)[1]
        else:
            u_shape_framework_conf_name = conf_module_name
        self._user_manager = UserManager(user_management_path, u_shape_framework_conf_name=u_shape_framework_conf_name)
        super(MultiUserEngine, self).__init__(conf_module, user_manager=self._user_manager)

    def get_user_manager(self):
        return self._user_manager

    def _parse_conf(self):
        processor_conf_list = copy.deepcopy(self._conf_module.processor_conf_list)
        workflow_conf_dict = copy.deepcopy(self._conf_module.workflow_conf_dict)
        return processor_conf_list, workflow_conf_dict

    def destroy(self):
        global _engine
        _engine = None
