# coding: utf-8
import os

import tornado
import tornado.httpclient
import tornado.ioloop
import tornado.web
import u_shape_framework
from u_shape_framework.engine import initialize_engine

# from classify_extract.app.online.classify_models_manager import ClassifyModelsManager
from classify_extract.app.online.classify_predictor import ClassifyPredictor
from classify_extract.app.driver import logger_online as logger
from classify_extract.app.handlers.predict_handlers import PredictHandler, PredictPathHandler, PredictByFieldsHandler,MainHandler
from classify_extract.app.handlers.reload_handler import ReloadHandler
from classify_extract.conf import conf
from classify_extract.conf import u_shape_framework_conf



import tornado.ioloop
import tornado.web


class Server(object):

    def __init__(self, output_dir, tmp_dir, upload_dir, port, model_links_dir='model', config_links_dir='config'):
        # if not os.path.exists(output_dir):
        #     raise ValueError('参数output_dir目录并不存在'.encode('utf-8'))
        # if not os.path.exists(tmp_dir):
        #     raise ValueError('参数tmp_dir目录并不存在'.encode('utf-8'))
        # if not os.path.exists(upload_dir):
        #     raise ValueError('参数upload_dir目录并不存在'.encode('utf-8'))
        # if not isinstance(port, int) or port <= 0 or port > 65535:
        #     raise ValueError('参数port必须合法(0~65535)')

        self._output_dir = output_dir
        self._tmp_dir = tmp_dir
        self._upload_dir = upload_dir
        self._port = port
        self._model_links_dir = model_links_dir
        self._config_links_dir = config_links_dir

        u_shape_framework.set_logger(logger)
        logger.info('initializing u_shape_framework engine ...')
        initialize_engine(u_shape_framework_conf)
        logger.info('engine initialize finish')

    def start(self):

        # models_manager = ClassifyModelsManager(self._output_dir, ClassifyPredictor, logger, self._model_links_dir,
        #                                        self._config_links_dir)
        logger.info('start server...')
        app = tornado.web.Application(
            handlers=[
                (conf.PREDICT_ROUTER, PredictHandler,
            #      {
            #     # 'models_manager': models_manager,
            #     'tmp_dir': self._tmp_dir,
            #     'upload_dir': self._upload_dir
            # }
                 ),
                      (conf.PREDICT_PATH_ROUTER, PredictPathHandler, {
                          # 'models_manager': models_manager,
                          'tmp_dir': self._tmp_dir,
                          'upload_dir': self._upload_dir
                      }), (conf.RELOAD_ROUTER, ReloadHandler, {
                    # 'models_manager': models_manager
                }),
                      (conf.PREDICT_BY_FIELDS, PredictByFieldsHandler, {
                          # 'models_manager': models_manager,
                          'tmp_dir': self._tmp_dir,
                          'upload_dir': self._upload_dir
                      })])
        app.listen(address='0.0.0.0', port=self._port)
        logger.info('server starts with address: 0.0.0.0, port: {}'.format(self._port))
        tornado.ioloop.IOLoop.current().start()
