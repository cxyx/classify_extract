#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Yang Huiyu
# @Date  : 2018/8/13
import codecs
import unittest

from HTMLTestRunner import HTMLTestRunner

suite = unittest.TestSuite()
suite.addTests(unittest.TestLoader().discover('.'))
with codecs.open('tests/environment/TestReport.html', 'w', 'utf-8') as f:
    runner = HTMLTestRunner(stream=f, title='Test Report', verbosity=2)
    result = runner.run(suite)
    if result.failure_count or result.error_count:
        exit(-1)
