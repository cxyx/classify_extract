# coding: utf-8
import unittest

import u_shape_framework

from classify_extract.app.driver import logger_online as logger


class Test(unittest.TestCase):

    def setUp(self):
        # init u_shape_engine
        u_shape_framework.set_logger(logger)
        logger.info('initializing u_shape_framework engine ...')
        pass

    def test_online_workflow(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
