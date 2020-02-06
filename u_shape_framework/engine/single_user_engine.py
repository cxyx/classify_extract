# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import copy
import importlib
import os
import sys
import threading
from time import sleep

from .. import get_logger
from typing import Text, Any
from ..conf_merger import ConfMerger
from .base_engine import BaseEngine


class SingleUserEngine(BaseEngine):

    def __init__(self, conf_module, override_conf_module_path=None, monitor_mode='auto'):
        # type: (Any, Any, Text) -> None
        self._check_update_thread = None
        self._override_conf_module_path = override_conf_module_path
        super(SingleUserEngine, self).__init__(conf_module)
        if self._override_conf_module_path and monitor_mode == 'auto':
            self._auto_monitor_override_module()

    def _parse_conf(self):
        processor_conf_list = copy.deepcopy(self._conf_module.processor_conf_list)
        workflow_conf_dict = copy.deepcopy(self._conf_module.workflow_conf_dict)
        if self._override_conf_module_path:
            try:
                override_conf_module_path = os.path.dirname(self._override_conf_module_path)
                if override_conf_module_path not in sys.path:
                    sys.path.append(os.path.dirname(self._override_conf_module_path))
                override_conf_module = importlib.import_module(os.path.basename(self._override_conf_module_path))
                if sys.version > '3':
                    importlib.reload(override_conf_module)
                else:
                    reload(override_conf_module)
                ConfMerger.merge_processor_conf_lists(processor_conf_list, override_conf_module.processor_conf_list)
                ConfMerger.merge_workflow_conf_dicts(workflow_conf_dict, override_conf_module.workflow_conf_dict)
            except Exception as e:
                get_logger().debug('cannot load override conf module, message {}'.format(str(e)))
        return processor_conf_list, workflow_conf_dict

    def update(self):
        modified_processor_conf_list, modified_workflow_conf_dict = self._parse_conf()

        different_processor_conf_list = ConfMerger.find_difference_in_processor_conf_lists(
            self._processor_conf_list, modified_processor_conf_list)
        if different_processor_conf_list:
            self._load_processors(different_processor_conf_list)
            self._processor_conf_list = modified_processor_conf_list
            self._load_workflows(self._workflow_conf_dict)

        different_workflow_conf_dict = ConfMerger.find_difference_in_workflow_conf_dicts(
            self._workflow_conf_dict, modified_workflow_conf_dict)
        if different_workflow_conf_dict:
            self._load_workflows(different_workflow_conf_dict)
            self._workflow_conf_dict = modified_workflow_conf_dict

    def _auto_monitor_override_module(self):
        self._check_update_thread = CheckUpdateThread(self)
        self._check_update_thread.setDaemon(True)
        self._check_update_thread.start()

    def destroy(self):
        if self._check_update_thread:
            self._check_update_thread.stop()
        global _engine
        _engine = None


class CheckUpdateThread(threading.Thread):

    def __init__(self, engine, interval=1):
        # type: (SingleUserEngine, float) -> CheckUpdateThread
        super(CheckUpdateThread, self).__init__()
        self._engine = engine
        self._interval = interval
        self._check = True

    def run(self):
        while self._check:
            sleep(self._interval)
            self._engine.update()

    def stop(self):
        self._check = False
