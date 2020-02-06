# -*- coding: utf-8 -*-
import requests
import os
import shutil
import pandas as pd
from u_shape_framework.processors.processor_base import ProcessorBase
from classify_extract.conf import conf
from classify_extract.app.utils.data_util import test_parse_tagged_data

from classify_extract.app.driver import generate_request_id, logger_offline as logger



class ProcessorDataPreprocess(ProcessorBase):

    def load(self, args):
        self._args = args

    def up(self, tmp_result, output, request_property):
        pass

    def down(self, tmp_result, output, request_property):
        logger.info('====================================================================')
        # data_path = request_property['field_config'].data_path #todo:删除
        data_path = '/Users/chenxuan/workspace/classify_extract/tests/test_data/input/20190515195025_81_355/process'

        version = request_property['field_config'].version
        classify_model_config = conf.field_config

        task_type = 'train'
        event_id = ''  # todo:待定
        label_dict = {}  # todo:待定
        use_rule = 0  # todo:待定

        csv_dir = self.txt2csv(data_path)

        configs = {
            'version': version,
            'task_type': task_type,  # 'train'或'evaluate'
            'event_id': event_id,  # model_train_id/model_evaluate_id
            'configs': classify_model_config,
            'data_path': csv_dir,  # 训练、评估样本数据路径
            'label_dict': dict,  # 类别id与类别名称的对应关系
            'use_rule': int,  # 0或1, 1代表使用规则
        }
        logger.info(configs)
        output['configs'] = configs

    @staticmethod
    def txt2csv(file_dir):
        csv_dir = os.path.join(file_dir, 'csv')

        if os.path.exists(csv_dir):
            shutil.rmtree(csv_dir)
            os.mkdir(csv_dir)
        else:
            os.mkdir(csv_dir)

        csv_path = csv_dir + '/train.csv'

        all_data_list = []
        for files in os.listdir(file_dir):  # 不仅仅是文件，当前目录下的文件夹也会被认为遍历到
            if files.endswith('.txt'):
                csv_file_path = file_dir + '/' + files
                field_id = files.split('_')[0]
                list3 = test_parse_tagged_data(csv_file_path, field_id)
                all_data_list = all_data_list + list3
        name = ['label', 'text', 'title', 'content', 'item_info']
        test = pd.DataFrame(columns=name, data=all_data_list)  # 数据有三列，列名分别为one,two,three
        test.to_csv(csv_path, encoding='utf-8', index=False)
        print('data_pre')
        return csv_dir
