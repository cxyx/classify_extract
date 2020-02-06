# coding=utf-8
import codecs
import json
import time

import tornado.web
# from extract_framework.models_manager.models_manager import ModelsManager

from u_shape_framework.engine import get_current_engine
from classify_extract.app.driver import generate_request_id, logger_online as logger


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print('MainHandler')
        self.write("Hello, world")

    def post(self):
        print('post')

class PredictHandler(tornado.web.RequestHandler):

    # def initialize(self, models_manager, tmp_dir, upload_dir):
        # if not isinstance(models_manager, ModelsManager):
        #     raise ValueError('参数models_manager必须是ModelsManager的实例'.encode('utf-8'))
        # self.models_manager = models_manager
        # self.tmp_dir = tmp_dir
        # self.upload_dir = upload_dir

    def predict(self, doctype, content, rich_content, fields=()):
        workflow_name = 'online'
        workflow = get_current_engine().get_workflow('online')
        logger.info('start to run {} workflow'.format(workflow_name))
        request_property = {
            # 'models_manager': self.models_manager,
            'doctype': doctype,
            'rich_content': rich_content,
            'content': content,
        }
        if fields:
            request_property['fields'] = fields
        output = workflow.run(request_property)
        result = {
            'result': '',
        }
        return result

    def get(self):
        print('1111111111111111')

    # @tornado.web.asynchronous
    # @tornado.gen.coroutine
    def post(self):
        print('extractextractextract')
        result = {'status': 'OK', 'msg': ''}
        print('extractextractextract')
        init_time = time.time()
        try:
            data = json.loads(self.request.body)
            caller_request_id = data.get('caller_request_id', None)
            self_request_id = generate_request_id()
            logger.update_logger_extra({'caller_request_id': caller_request_id, 'self_request_id': self_request_id})
            doctype, content, rich_content = str(data['doctype']), data['content'], data['rich_content']
            # logger.info('received data keys: {}, doctype: {}, content: {} ......'.format(
            #     list(data.keys()), doctype, content[:100]))
            # self.predict(doctype, content, rich_content)
            result.update(self.predict(doctype, content, rich_content))
        except Exception as e:
            result['status'] = 'ERROR'
            result['msg'] = '{}'.format(e)
            logger.exception(e)
        result_str = json.dumps(result, ensure_ascii=False)
        self.write(result_str)
        logger.info('results: {}, cost time: {}s'.format(result_str, time.time() - init_time))
        logger.update_logger_extra()


class PredictPathHandler(PredictHandler):

    # @tornado.web.asynchronous
    # @tornado.gen.coroutine
    def post(self):
        result = {'status': 'OK', 'msg': ''}
        init_time = time.time()
        try:
            data = json.loads(self.request.body)
            caller_request_id = data.get('caller_request_id', None)
            self_request_id = generate_request_id()
            logger.update_logger_extra({'caller_request_id': caller_request_id, 'self_request_id': self_request_id})
            doctype, content, rich_content_path = str(data['doctype']), data['content'], data['rich_content_path']
            logger.info('received data keys: {}, doctype: {}, content: {} ......'.format(
                list(data.keys()), doctype, content[:100]))
            with codecs.open('{}/{}'.format(self.upload_dir, rich_content_path)) as f:
                rich_content = json.loads(f.read())
            result.update(self.predict(doctype, content, rich_content))
        except Exception as e:
            result['status'] = 'ERROR'
            result['msg'] = '{}'.format(e)
            logger.exception(e)
        result_str = json.dumps(result, ensure_ascii=False)
        self.write(result_str)
        logger.info('results: {}, cost time: {}s'.format(result_str, time.time() - init_time))
        logger.update_logger_extra()


class PredictByFieldsHandler(PredictHandler):

    # @tornado.web.asynchronous
    # @tornado.gen.coroutine
    def post(self):
        result = {'status': 'OK', 'msg': ''}
        init_time = time.time()
        try:
            data = json.loads(self.request.body)
            caller_request_id = data.get('caller_request_id', None)
            self_request_id = generate_request_id()
            logger.update_logger_extra({'caller_request_id': caller_request_id, 'self_request_id': self_request_id})
            doctype, content, rich_content, fields = str(data['doctype']), data['content'], \
                                                     data['rich_content'], data['fields']
            logger.info('received data keys: {}, doctype: {}, fields: {}, content: {} ......'.format(
                list(data.keys()), doctype, fields, content[:100]))
            if not isinstance(fields, list):
                raise ValueError('args: fields must be list')
            result.update(self.predict(doctype, content, rich_content, fields))
        except Exception as e:
            result['status'] = 'ERROR'
            result['msg'] = '{}'.format(e)
            logger.exception(e)
        result_str = json.dumps(result, ensure_ascii=False)
        self.write(result_str)
        logger.info('results: {}, cost time: {}s'.format(result_str, time.time() - init_time))
        logger.update_logger_extra()
