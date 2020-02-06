# coding: utf-8
import sys
import os
import pandas as pd
import codecs
from classify_extract.app.utils import data_util


def test_parse_tagged_data(data_path, field_id):
    list = []

    for content, label_indices in data_util.parse_tagged_data(data_path):
        for i in label_indices:
            field_list = []
            field_list.append(field_id)
            field_list.append(content[i[0]:i[1]])
            field_list.extend(['', '', ''])
            list.append(field_list)

    return list


def list2csv(list, file):
    name = ['label', 'text', 'title', 'content', 'item_info']
    test = pd.DataFrame(columns=name, data=list)  # 数据有三列，列名分别为one,two,three
    test.to_csv(file, encoding='utf-8', index=False)


def file_name_listdir(file_dir, output_path):
    all_data_list = []
    for files in os.listdir(file_dir):  # 不仅仅是文件，当前目录下的文件夹也会被认为遍历到
        if files.endswith('.txt'):
            csv_file_path = file_dir + '/' + files
            field_id = files.split('_')[0]
            list3 = test_parse_tagged_data(csv_file_path, field_id)
            all_data_list = all_data_list + list3
    list2csv(all_dpata_list, output_path)


if __name__ == '__main__':
    file_dir = '/Users/chenxuan/PycharmProjects/code_test/input/20190515195025_81_355/process'
    output_path = 'test111.csv'
    file_name_listdir(file_dir, output_path)
