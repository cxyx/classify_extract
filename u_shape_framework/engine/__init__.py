# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

from .. import get_logger
from typing import Text
from .single_user_engine import SingleUserEngine
from .multi_user_engine import MultiUserEngine

_engine = None


class Status(object):
    NotInitialized = 'not_initialized'
    Initializing = 'initializing'
    Success = 'success'
    Failed = 'failed'


_status = Status.NotInitialized


def get_status():
    # type: () -> Text
    return _status


def get_current_engine():
    if _status == Status.NotInitialized:
        raise RuntimeError('Engine is not initialized')
    elif _status == Status.Initializing:
        raise RuntimeError('Engine is initializing')
    elif _status == Status.Failed:
        raise RuntimeError('Engine is failed to initialize')
    else:
        return _engine


def initialize_engine(conf_module, override_conf_module_path=None, monitor_mode='auto'):
    return initialize_single_user_engine(conf_module,
                                         override_conf_module_path=override_conf_module_path,
                                         monitor_mode=monitor_mode)


def initialize_single_user_engine(conf_module, override_conf_module_path=None, monitor_mode='auto'):
    """
    默认配置模块+override配置模块，此模式支持额外的参数monitor_mode，可以为auto或者manual。
    auto模式下每隔1s会根据override配置模块自动更新一次配置，manual则不会自动更新，需要手动更新。
    当构造函数中传入user_management_path时，会触发多租户模式，否认为单租户模式。
    :param conf_module: 默认配置模块，单租户时，每个processor的配置项目包括name、module和args。
                        多租户时，则需要配置name、module即可，args统一由多租户模块进行管理。
    :param override_conf_module_path: 单租户模式下，会覆盖对应processor的默认args及workflow的构成。
    :param monitor_mode: 单租户模式下，读取override模块更新配置的模式，支持auto和manual两种模式，auto模式会每隔1s自动更新，manual模式下需要手动更新。
    :return: engine初始化的结果，success或failed。
    """
    global _status
    _status = Status.Initializing
    try:
        global _engine
        _engine = SingleUserEngine(
            conf_module=conf_module,
            override_conf_module_path=override_conf_module_path,
            monitor_mode=monitor_mode,
        )
        _status = Status.Success
    except Exception as e:
        get_logger().exception(str(e))
        _status = Status.Failed
    return _status


def initialize_multi_user_engine(conf_module, user_management_path):
    global _status
    _status = Status.Initializing
    try:
        global _engine
        _engine = MultiUserEngine(conf_module=conf_module, user_management_path=user_management_path)
        _status = Status.Success
    except Exception as e:
        get_logger().exception(str(e))
        _status = Status.Failed
    return _status
