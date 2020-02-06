# coding: utf-8
import codecs


def parse_tagged_data(data_path):
    """
    解析\3\4标注数据
    :param data_path: 
    :return: 
    """
    for line in codecs.open(data_path, 'r', 'utf-8'):
        line = line.strip()
        if line:
            content = ''
            label_indices = []
            for term in line.split('\3'):
                value, tag = term.split('\4')
                content += value
                if tag != 'O':
                    start_idx = content.rindex(value)
                    end_idx = start_idx + len(value)
                    label_indices.append([start_idx, end_idx])
            yield content, label_indices


def test_parse_tagged_data(data_path, field_id):
    result_list = []

    for content, label_indices in parse_tagged_data(data_path):
        for i in label_indices:
            field_list = []
            field_list.append(field_id)
            field_list.append(content[i[0]:i[1]])
            field_list.extend(['', '', ''])
            print('list1', field_list)
            result_list.append(field_list)

    return result_list