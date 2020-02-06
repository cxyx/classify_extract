# coding: utf-8
import unittest

import u_shape_framework
from u_shape_framework.engine import initialize_engine

from classify_extract.app.driver import logger_offline as logger
from classify_extract.conf import u_shape_framework_conf


class Test(unittest.TestCase):

    def setUp(self):
        # init u_shape_engine
        u_shape_framework.set_logger(logger)
        logger.info('initializing u_shape_framework engine ...')
        initialize_engine(u_shape_framework_conf)
        logger.info('engine initialize finish')
        pass

    def test_offline_workflow(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
