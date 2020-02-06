# coding=utf-8
# email:  lihanqing@datagrand.com
# create: 2019-05-15-11:55
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import sys
import importlib
import os
import copy

from .conf_merger import ConfMerger
from . import get_logger


class UserManager(object):

    def __init__(self,
                 user_management_path,
                 u_shape_framework_conf_name='u_shape_framework_conf',
                 system_conf_folder='system_conf',
                 user_conf_folder='user_conf',
                 default_user_name='default'):
        self._user_management_path = os.path.abspath(user_management_path)
        sys.path.insert(0, self._user_management_path)
        self._u_shape_framework_conf_name = u_shape_framework_conf_name
        self._system_conf_folder = system_conf_folder
        self._user_conf_folder = user_conf_folder
        self._default_user_name = default_user_name
        self._user_conf_path = os.path.join(self._user_management_path, user_conf_folder)

    def get_user_u_shape_framework_conf(self, user_id, processor_name, default_args):
        try:
            processor_conf_list = self._load_variance(user_id, self._u_shape_framework_conf_name, 'processor_conf_list')
            for processor_conf in processor_conf_list:
                if processor_conf['name'] == processor_name:
                    user_args = copy.deepcopy(default_args)
                    ConfMerger.merge_dict(user_args, processor_conf['args'])
                    return user_args
            else:
                return default_args
        except Exception as e:
            get_logger().warning('Can\'t load user: {}, processor: {} args, use system args, message: {}'.format(
                user_id, processor_name, str(e)))
            return default_args

    def get_user_conf(self, user_id, module_name, variance_name):
        try:
            variance = self._load_variance(user_id, module_name, variance_name)
            if isinstance(variance, dict):
                system_variance = self.get_system_conf(module_name, variance_name)
                ConfMerger.merge_dict(system_variance, variance)
                variance = system_variance
        except Exception as e:
            if user_id == self._default_user_name:
                get_logger().warning(
                    'Can\'t load user: default, processor: {} args, use system args, message: {}'.format(
                        module_name, str(e)))
                variance = self.get_system_conf(module_name, variance_name)
            else:
                variance = self.get_user_conf(self._default_user_name, module_name, variance_name)
        return variance

    def get_system_conf(self, module_name, variance_name):
        conf_module = importlib.import_module(self._system_conf_folder + '.' + module_name)
        variance = getattr(conf_module, variance_name)
        return variance

    def get_user_conf_module(self, user_id, module_name):
        try:
            self._reload_module(user_id)
            conf_module = self._reload_module(user_id + '.' + module_name)
        except Exception as e:
            get_logger().warning('Can\'t load module {} from user {}, message'.format(module_name, user_id, str(e)))
            conf_module = None
        return conf_module

    def get_user_conf_path(self, user_id):
        return os.path.join(self._user_conf_path, user_id)

    def get_user_id_list(self):
        user_id_list = []
        if os.path.exists(self._user_conf_path):
            for user_id in os.listdir(self._user_conf_path):
                user_path = os.path.join(self._user_conf_path, user_id)
                if os.path.isdir(user_path):
                    user_id_list.append(user_id)
        return user_id_list

    def _load_variance(self, user_id, module_name, variance_name):
        self._reload_module(self._user_conf_folder + '.' + user_id)
        conf_module = self._reload_module(self._user_conf_folder + '.' + user_id + '.' + module_name)
        variance = getattr(conf_module, variance_name)
        return variance

    def _reload_module(self, module_name):
        module = importlib.import_module(module_name)
        if sys.version > '3':
            importlib.reload(module)
        else:
            reload(module)
        return module
