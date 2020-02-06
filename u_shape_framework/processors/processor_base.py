# coding=utf-8
# email:  xgao85@gmail.com
# create: 2016年12月14日-下午4:21
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import abc
from typing import Dict, Text
from .. import get_logger


class ProcessorBase(object):
    '''
    processor base class
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self, name, processor_args, comment='', user_manager=None):
        self._name = name
        self._comment = comment
        self._user_manager = user_manager
        self._processor_args = processor_args
        self.load(processor_args)

    @property
    def name(self):
        return self._name

    @property
    def comment(self):
        return self._comment

    @property
    def user_manager(self):
        return self._user_manager

    @property
    def args(self):
        return self._processor_args

    @abc.abstractmethod
    def load(self, processor_args):
        pass

    @abc.abstractmethod
    def up(self, tmp_result, output, request_property):
        # type: (Dict, Dict, Dict) -> None
        pass

    @abc.abstractmethod
    def down(self, tmp_result, output, request_property):
        # type: (Dict, Dict, Dict) -> None
        pass

    def process(self, tmp_result, output, request_property):
        # type: (Dict, Dict, Dict) -> Text
        direction = self.direction_controller(tmp_result, output, request_property)
        if self._user_manager:
            enable = self.get_user_args(request_property).get('enable', True)
        else:
            enable = self._processor_args.get('enable', True)
        if enable:
            get_logger().debug('processor: {}, \"{}\" method start'.format(self.name, direction))
            if direction == 'up':
                self.up(tmp_result, output, request_property)
            elif direction == 'down':
                self.down(tmp_result, output, request_property)
            else:
                raise RuntimeError('direction error, please check your code, direction is {}.'.format(direction))
            hook_direction = self.direction_hook(tmp_result, output, request_property)
            if hook_direction:
                get_logger().debug('processor: {}, \"{}\" method end, next direction: \"{}\"'.format(
                    self.name, direction, hook_direction))
                direction = hook_direction
            else:
                get_logger().debug('processor: {}, \"{}\" method end, next direction: \"{}\"'.format(
                    self.name, direction, direction))
        else:
            get_logger().info('processor {} is disabled, {} directly'.format(self.name, direction))
        return direction

    def direction_hook(self, tmp_result, output, request_property):
        return ''

    def direction_controller(self, tmp_result, output, request_property):
        # type: (Dict, Dict, Dict) -> Text
        run_flag = self.get_run_flag(request_property)
        if run_flag:
            self.set_run_flag(request_property, False)
            return 'up'
        else:
            self.set_run_flag(request_property, True)
            return 'down'

    def get_global_variance(self, request_property):
        processor_id = self._get_processor_id(request_property)
        global_variance_dict = request_property['run_info']['global_variance_dict']
        if processor_id not in global_variance_dict:
            global_variance_dict[processor_id] = {}
        return global_variance_dict[processor_id]

    def _get_user_id(self, request_property):
        if self._user_manager:
            user_id = request_property['user_id']
        else:
            raise RuntimeError('Single user mode, no user id')
        return user_id

    def get_user_args(self, request_property):
        if self._user_manager:
            user_args = request_property['user_args'][self.name]
        else:
            raise RuntimeError('Single user mode, no user args')
        return user_args

    def get_run_flag(self, request_property):
        processor_id = self._get_processor_id(request_property)
        run_flag_dict = request_property['run_info']['run_flag_dict']
        if processor_id not in run_flag_dict:
            run_flag_dict[processor_id] = False
        return run_flag_dict[processor_id]

    def set_run_flag(self, request_property, value):
        processor_id = self._get_processor_id(request_property)
        request_property['run_info']['run_flag_dict'][processor_id] = value

    def _get_processor_id(self, request_property):
        current_index = request_property['run_info']['current_index']
        processor_id = '{}_{}'.format(current_index, self._name)
        return processor_id
