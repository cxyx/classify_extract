# -*- coding: utf-8 -*-
import re
import traceback
import sys
import requests
from classify_extract.conf.conf import SPLIT_SIGN_DICT
import json
from classify_extract.app.driver import generate_request_id, logger_online as logger
from classify_extract.conf.conf import CLASSIFY_PORT


def cut_head(text, head):
    result = re.search(head, text)
    if result:
        return len(result.group())
    else:
        return 0


return_items = {}


def extract_approval_opinion(sents_map, model_dir):
    text, mapper = sents_map[0], sents_map[1]
    sent_list = re.split(r'。', text)
    print('sent_list', sent_list)

    mapper_index = 0
    for each in sent_list:
        print('each', each)
        if each != '':
            field_id, prob = extract(each, model_dir)
            if field_id not in return_items:
                return_items[field_id] = []
            return_items.get(field_id).append([each, prob, mapper[mapper_index]])
            mapper_index += len(each) + 1
    return return_items


def solve(cuted_sent_dict, up_type=r'非承诺'):
    return_items = []
    result = cuted_sent_dict.get('result', [])
    cur_type = cuted_sent_dict.get(r'type', '非承诺') if up_type != up_type != r'承诺' else up_type
    for each in result:
        if isinstance(each, list):
            each.append(cur_type)
            return_items.append(each)
        else:
            return_items.extend(solve(each, cur_type))

    return return_items


def extract_preconditions(sents_map, model_dir):
    cuted_sent_dict = cut_prerequisite(sents_map, r'非承诺')  #
    # return_items = {u'high': [], u'mid': [], u'low': []}
    # return_items = {}
    tk_list = solve(cuted_sent_dict)

    # re_compile_list_high = PRECONDITIONS_HIGH
    # re_compile_list_MID = PRECONDITIONS_MID

    for each_tk in tk_list:
        tk_content = each_tk[0]
        tk_start_idx = each_tk[1]
        tk_type = each_tk[2]
        print('tk_content......................', tk_content)
        field_id, prob = extract(tk_content, model_dir)
        if field_id not in return_items:
            return_items[field_id] = []
        return_items.get(field_id).append([tk_content, prob, tk_start_idx])

    logger.info('extract_preconditions::{}'.format(return_items))
    return return_items


def extract_management_condition(sent_map, model_dir):
    text, all_mapper = sent_map[0], sent_map[1]
    each_index = 0
    re_compile_mid = []
    each_index = 0
    each_sent_list_juhao = re.split(r'[；; 。]', text)
    for each_sent in each_sent_list_juhao:
        if not each_sent.replace(r' ', ''):
            each_index += len(each_sent) + 1
            continue
        field_id, prob = extract(each_sent, model_dir)

        if field_id not in return_items:
            return_items[field_id] = []
        return_items.get(field_id).append([each_sent, prob, all_mapper[each_index]])

        each_index += len(each_sent) + 1
    logger.info('extract_management_condition::{}'.format(return_items))
    return return_items


def cut_prerequisite_nosign(text, mapper, type):
    return_items = re.split(r'[；;。]', text)
    return_items_ = {'result': [], 'type': type}
    index = 0
    for item in return_items:
        if not re.sub(r'\s', r'', item):
            index += len(item) + 1
            continue
        return_items_['result'].append([item, mapper[index]])
        index += len(item) + 1
    return return_items_


def cut_prerequisite(prerequisite, type):
    CNYD_REG = re.compile(r'[^0-9：:]+[:：]')
    return_items = {'result': [], 'type': type}

    if not prerequisite:
        return return_items

    text, mapper = prerequisite[0], prerequisite[1]
    logger.info('前提条件文本内容:{}'.format(text))
    reg_1 = re.compile(r'[  1一、.（）\s]+')
    result_reg_1 = reg_1.match(text)
    split_sign = result_reg_1.group() if result_reg_1 else 'xxx'
    split_sign = re.sub(r'[\s  ]', r'', split_sign)

    if split_sign not in SPLIT_SIGN_DICT:
        cnyd_result = CNYD_REG.match(text)
        if not cnyd_result:
            return_items['result'].append(cut_prerequisite_nosign(text, mapper, type))

        else:
            if re.search(r'承诺|约定|访谈|书面记录|(协议|合同).*[增添]加', cnyd_result.group()):
                return_items['type'] = r'承诺'
            return_items['result'].append(
                {'result': [[cnyd_result.group(), mapper[cnyd_result.start()]]], 'type': return_items['type']})
            start, end = cnyd_result.span()
            return_items['result'].append(
                cut_prerequisite([text[end:], mapper[end:]], return_items['type']))

    else:
        split_sign_reg = SPLIT_SIGN_DICT[split_sign]
        split_sign_len = len(split_sign)
        splited_ = re.split(split_sign_reg, text)
        index = 0
        for idx, each in enumerate(splited_[:]):
            if re.sub(r'\s', r'', each):
                return_items['result'].append(
                    cut_prerequisite([each, mapper[index:index + len(each)]], return_items['type']))
            index += len(each) + split_sign_len
    return return_items


def start_extract(opontions, prerequisite, requirement, model_dir):
    try:
        items1 = extract_approval_opinion(opontions, model_dir) if opontions else {}
        print('items1items1', items1)

    except Exception as e:
        logger.error('抽取审批意见报错')
        logger.error(e)
        items1 = {}

    try:
        items2 = extract_preconditions(prerequisite, model_dir) if prerequisite else {}
        print('items2items2', items2)

    except Exception as e:
        logger.error('抽取前提条件报错')
        logger.error(str(e) + traceback.format_exc())
        items2 = {}

    try:
        items3 = extract_management_condition(requirement, model_dir) if requirement else {}
        print('items3items3', items3)

    except Exception as e:
        logger.error('抽取管理要求报错')
        logger.error(e)
        items3 = {}
    logger.info('start_extract::{}'.format(return_items))
    return return_items


def extract(sentence, url):
    msg = {'app_id': '',
           'text': sentence,
           'category': '',
           'use_rule': ''  # todo:准备request请求,

           }
    url = 'http://{}:{}/classify'.format('127.0.0.1', CLASSIFY_PORT)  #todo:服务器的映射的port,host把端口的添加到噢诶之文件中
    data = json.loads(requests.get(url, data=json.dumps(msg)))
    label_name = data.result[0]['label_name']
    prob = data.result[0]['prob']
    return label_name, prob
