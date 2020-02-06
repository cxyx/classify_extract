# coding=utf-8
from u_shape_framework.engine import get_current_engine

from classify_extract.app.driver import logger_online as logger


class ClassifyPredictor(object):

    def __init__(self, model_path):
        pass

    def predict(self, content, field_config):
        logger.info('start to run online workflow')
        workflow = get_current_engine().get_workflow('otonline')
        request_property = {'content': content, 'field_config': field_config}
        output = workflow.run(request_property)
        result = output['results']
        return result
