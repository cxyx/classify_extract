# coding: utf-8
import unittest
import json

from classify_extract.app.utils import data_util


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def test_parse_tagged_data(self):
        print('test_parse_tagged_data~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        data_path = 'tests/test_data/input/20190515195025_81_355/process/1518_data.txt'
        for content, label_indices in data_util.parse_tagged_data(data_path):
            print(('content: {}'.format(json.dumps(content, ensure_ascii=False))))
            print(('labels: {}'.format(json.dumps(label_indices, ensure_ascii=False))))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
