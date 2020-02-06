#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-11-27 10:27
# @Author  : zhangyicheng@datagrand.com
from __future__ import unicode_literals

import copy
import logging
import sys
import time


class StdoutLevelFilter(object):

    @staticmethod
    def filter(record):
        if record.levelno in [logging.DEBUG, logging.INFO]:
            return True
        return False


class DgFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
            s = '%s,%03d%s' % (t, record.msecs, time.strftime('%z'))
        return s


global_config_dict = {
    'version': 1,
    'disable_existing_loggers': True,
    'incremental': False,
    'formatters': {
        'standard': {
            'class': 'dg_logging.templates.config_dicts.DgFormatter',
            'format': '',
        },
    },
    'filters': {
        'stdout_filter': {
            '()': 'dg_logging.templates.config_dicts.StdoutLevelFilter'
        },
    },
    'handlers': {
        'stdout_stream_handler': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filters': [
                'stdout_filter',
            ],
            'stream': 'ext://sys.stdout',
        },
        'stderr_stream_handler': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'formatter': 'standard',
            'stream': 'ext://sys.stderr'
        },
    },
    'loggers': {},
}

format_templates = {

    # template 1
    1:
    '%(asctime)s - %(caller_request_id)s - %(self_request_id)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s() - %(message)s',

}

logger_conf = {
    'handlers': ['stdout_stream_handler', 'stderr_stream_handler'],
    'level': 'DEBUG',
    'qualname': 'default',
}


def get_log_conf_dict(name, template_id, log_file_path, propagate):
    log_format = _get_log_format(template_id)
    _set_log_format(log_format)
    file_handler_conf_dict = _gen_file_handler_conf_dict(log_file_path)
    handler_name = _add_handler(name, file_handler_conf_dict)
    logger_conf_dict = _gen_logger_conf_dict(handler_name, propagate)
    _add_logger(name, logger_conf_dict)
    return global_config_dict


def _get_log_format(template_id):
    if template_id not in format_templates:
        template_num = max(format_templates.keys())
        raise Exception(
            'We only provide {} templates, please read the documentation and give a valid integer for template'
            ' between 1 and {}'.format(template_num, template_num))
    return format_templates[template_id]


def _set_log_format(log_format):
    current_format = global_config_dict['formatters']['standard']['format']
    if current_format and current_format != log_format:
        print('Warning: overwriting an existing format')
    global_config_dict['formatters']['standard']['format'] = log_format
    # as logging in python 2 does not support Format class, we use datefmt but the millisecond info is lost
    if sys.version < '3':
        global_config_dict['formatters']['standard'].update({
            'datefmt': '%Y-%m-%d %H:%M:%S%z'
        })


def _gen_file_handler_conf_dict(log_file_path):
    return {
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'level': 'DEBUG',
        'formatter': 'standard',
        'filename': log_file_path,
        'backupCount': 7,
        'when': 'D',
    }


def _add_handler(name, file_handler_conf_dict):
    if name is None:
        handler_name = 'file_handler'
    else:
        handler_name = name + '_file_handler'
    if handler_name in global_config_dict['handlers']:
        logging.getLogger().warning('modifying an existing handler conf: {}'.format(handler_name))
    global_config_dict['handlers'].update({handler_name: file_handler_conf_dict})
    return handler_name


def _gen_logger_conf_dict(handler_name, propagate):
    logger_conf_dict = copy.deepcopy(logger_conf)
    logger_conf_dict['handlers'].append(handler_name)
    logger_conf_dict['propagate'] = propagate
    return logger_conf_dict


def _add_logger(name, logger_conf_dict):
    if name is None:
        if 'root' in global_config_dict:
            logging.getLogger().warning('modifying existing root logger')
        global_config_dict.update({'root': logger_conf_dict})
    else:
        if name in global_config_dict['loggers']:
            logging.getLogger(name).warning('modifying an existing logger: {}'.format(name))
            logging.getLogger().warning('modifying an existing logger: {}'.format(name))
        global_config_dict['loggers'].update({name: logger_conf_dict})
