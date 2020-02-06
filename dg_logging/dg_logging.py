#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-11-26 12:10
# @Author  : zhangyicheng@datagrand.com
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import sys
import logging
import logging.config
import traceback

from functools import partial

from dg_logging.templates.config_dicts import get_log_conf_dict

DEFAULT_EXTRA_DICT = {'caller_request_id': None, 'self_request_id': None}


class DGLogger(logging.LoggerAdapter):

    def __init__(self, builder):
        self._name = builder.name
        self._extra_dict = builder.extra_dict
        self._template_id = builder.template_id
        self._log_file_path = os.path.abspath(builder.log_file_path)
        self._customized_config = builder.customized_config
        self._propagate = builder.propagate

        self._initialize()
        logger = logging.getLogger(self.name)
        super(DGLogger, self).__init__(logger, self.extra_dict)
        self.warn = self.warning
        self.fatal = self.critical
        self.exception = partial(self._exception, logger=self)

    @property
    def name(self):
        return self._name

    @property
    def extra_dict(self):
        return self._extra_dict

    @property
    def template_id(self):
        return self._template_id

    @property
    def log_file_path(self):
        return self._log_file_path

    @property
    def customized_config(self):
        return self._customized_config

    @property
    def propagate(self):
        return self._propagate

    def update_logger_extra(self, extra=None):
        """
        update logger adapter's extra, if extra_dict not given, extra will be re-initialized
        :param extra: a dict having all needed extra fields as keys, cf. DEFAULT_EXTRA_DICT.
        :return:
        """
        if extra is None:
            extra = DEFAULT_EXTRA_DICT
        self.extra = extra

    class Builder(object):

        def __init__(self):
            self._name = None
            self._extra_dict = DEFAULT_EXTRA_DICT
            self._template_id = 1
            self._log_file_path = '../log/root.log'
            self._customized_config = None
            self._propagate = True

        @property
        def name(self):
            return self._name

        def set_name(self, name):
            """
            :param name: name of the logger, support child logger calling it 'child logger' of a parent logger 'parent
             logger' by naming it as 'parent_name.child_name'
            :return:
            """
            self._name = name
            return self

        @property
        def extra_dict(self):
            return self._extra_dict

        def set_extra_dict(self, extra_dict):
            """
            :param extra_dict: extra information, if not set, it will get the DEFAULT_EXTRA_DICT defined above instead.
            :type extra_dict: dict
            :return:
            """
            self._extra_dict = extra_dict
            return self

        @property
        def template_id(self):
            return self._template_id

        def set_template_id(self, template_id):
            """
            :param template_id: decide which dict template will be used if using dict template.
            :return:
            """
            self._template_id = template_id
            return self

        @property
        def log_file_path(self):
            return self._log_file_path

        def set_log_file_path(self, log_file_path):
            """
            :param log_file_path: log file path if we choose to use a different one.
            :return:
            """
            self._log_file_path = log_file_path
            return self

        @property
        def customized_config(self):
            return self._customized_config

        def set_customized_config(self, customized_config):
            """
            :param customized_config: if use_template is set to False, a file log's path or a dict object should be input
        for configuring logging.
            :type customized_config: str or dict
            :return:
            """
            self._customized_config = customized_config
            return self

        @property
        def propagate(self):
            return self._propagate

        def set_propagate(self, propagate):
            """
            :param propagate: set the propagate param of the created logger
            :return:
            """
            self._propagate = propagate
            return self

        def build(self):
            return DGLogger(self)

    def _initialize(self):
        """
        initialize logger, should give a config file, file config as default, dict config will also be supported(which
        enables filters). Initialize extra for loggers.
        """
        if self.customized_config is None:  # use template
            config_dict = get_log_conf_dict(self.name, self.template_id, self.log_file_path, self.propagate)
            logging.config.dictConfig(config_dict)
        else:  # use customized config
            if isinstance(self.customized_config, str):
                logging.config.fileConfig(self.customized_config)
            elif isinstance(self.customized_config, dict):
                logging.config.dictConfig(self.customized_config)
            else:
                raise Exception('customized_config should be only a file log\'s path or a dict object.')

        if sys.version > '3':
            logging.Logger._log.__defaults__ = (None, self.extra_dict, False)
        else:
            logging.Logger._log.im_func.func_defaults = (None, self.extra_dict)

    @staticmethod
    def _exception(e, logger):
        logger.error('{}\t{}'.format(e, traceback.format_exc().replace('\n', ' ' * 4)))
