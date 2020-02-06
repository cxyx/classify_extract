# coding: utf-8
from extract_framework.models_manager.models_manager import ModelsManager

from classify_extract.app.driver import logger_online as logger


class ClassifyModelsManager(ModelsManager):

    def __init__(self, output_dir, model_class, logger=logger, model_links_dir='model', config_links_dir='config'):
        super(ClassifyModelsManager, self).__init__(output_dir,
                                                    model_class,
                                                    logger=logger,
                                                    model_links_dir=model_links_dir,
                                                    config_links_dir=config_links_dir)

    def _get_features(self, doctype, field, content):
        logger.info('get features for doctype: {}, field: {}'.format(doctype, field))
        return content

    def predict_for_field(self, doctype, field, content):
        features = self._get_features(doctype, field, content)
        return self.models[doctype][field].predict(features, self.fields_configs[doctype][field])
