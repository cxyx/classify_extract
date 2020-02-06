# -*- coding: utf-8 -*-
import re
import traceback
import sys
import requests
from ..driver import logger_online as logger
from classify_extract.conf import conf
from classify_extract.conf.conf import APPROVAL_OPINION_HIGH, MANAGEMENT_CONDITION_LOW_TO_HIGH, SPLIT_SIGN_DICT

sys.path.append('classify_extract/app/text_classification/src')

def cut_head(text, head):
    result = re.search(head, text)
    if result:
        return len(result.group())
    else:
        return 0


def extract_approval_opinion(sents_map, model_dir):
    logger.info('extract_approval_opinion:sents_map:{},model_dir:{}'.format(sents_map,model_dir))
    text, mapper = sents_map[0], sents_map[1]
    logger.info('text:{}, mapper:{}'.format(text, mapper))
    return_items = {'high': [], 'mid': [], 'low': []}

    sent_list = re.split(r'。', text)
    logger.info('sent_list{}'.format(sent_list))
    mapper_index = 0
    for each in sent_list:
        if mapper_index >= len(mapper):
            break
        if not each.replace(' ', ''):
            mapper_index += len(each) + 1
            continue

        for each_reg in APPROVAL_OPINION_HIGH:
            if re.search(each_reg, each):
                request_result = 'high'
                break
        else:
            request_result = 'low'
        if return_items == 'mid':
            return_items['high'].append([each, 1, mapper[mapper_index]])
        else:
            return_items[request_result].append([each, 1, mapper[mapper_index]])
        mapper_index += len(each) + 1
    return_items.pop('low')
    return return_items  #    return_items = {u'high': [[each, 1, mapper[mapper_index]],[each, 1, mapper[mapper_index]]], u'mid': [], u'low': []}


def solve(cuted_sent_dict, up_type = r'非承诺'):
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
    cuted_sent_dict = cut_prerequisite(sents_map, r'非承诺')
    return_items = {'high': [], 'mid': [], 'low': []}
    tk_list = solve(cuted_sent_dict)

    # re_compile_list_high = PRECONDITIONS_HIGH
    # re_compile_list_MID = PRECONDITIONS_MID

    for each_tk in tk_list:
        tk_content = each_tk[0]
        tk_start_idx = each_tk[1]
        tk_type = each_tk[2]

        filed, prob = classify_extract(tk_content, '前提条件', model_dir)

        # if not request_result in return_items:

        if request_result == 'high':
            if tk_type == '承诺':
                request_result = 'mid'
                return_items['mid'].append([tk_content, prob, tk_start_idx])
            else:
                return_items['high'].append([tk_content, prob, tk_start_idx])
        elif request_result == 'mid':
            request_result['mid'].append([[tk_content, tk_start_idx]])
        elif request_result == 'low':
            if tk_type == '承诺':
                if re.search(r'禁入领域', tk_content):
                    request_result = 'no_highlight'
                else:
                    request_result = 'mid'
                    return_items['mid'].append([tk_content, prob, tk_start_idx])
            else:
                request_result = 'no_highlight'
    logger.info('return_items|extract_preconditions{}'.format(return_items))
    return return_items


def extract_management_condition(sent_map, model_dir):
    text, all_mapper = sent_map[0], sent_map[1]
    return_iterms = {'high': [], 'mid': [], 'low': []}
    each_index = 0
    re_compile_mid = []
    each_index = 0
    each_sent_list_juhao = re.split(r'[；; 。]', text)
    for each_sent in each_sent_list_juhao:
        if not each_sent.replace(r' ', ''):
            each_index += len(each_sent) + 1
            continue
        request_result, prob = classify_extract(each_sent, '管理要求', model_dir)
        logger.info('extract_management_condition:0000000000[{}]111111111111[{}][{}]'.format(request_result,prob,each_sent))
        logger.info('all_mapper[each_index]{}'.format(all_mapper[each_index]))
        if request_result == 'high':
            return_iterms['high'].append([each_sent, prob, all_mapper[each_index]])
        elif request_result == 'mid':
            request_result = 'high'
            return_iterms['high'].append([each_sent, prob, all_mapper[each_index]])
        elif request_result == 'low':
            for each_reg in MANAGEMENT_CONDITION_LOW_TO_HIGH:
                if re.search(each_reg, each_sent):
                    request_result == 'high'
                    return_iterms['high'].append([each_sent, prob, all_mapper[each_index]])
                    break
            if re.search(r'审核时效|指定.*(负责人)', each_sent):
                request_result = 'no_hightlight'
            else:
                return_iterms['low'].append([each_sent, prob, all_mapper[each_index]])

        each_index += len(each_sent) + 1
    return return_iterms


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
    return_items = {'high': [], 'mid': [], 'low': []}
    try:
        items1 = extract_approval_opinion(opontions, model_dir) if opontions else {}
    except Exception as e:
        logger.error('抽取审批意见报错')
        logger.error(e)
        items1 = {}

    try:
        items2 = extract_preconditions(prerequisite, model_dir) if prerequisite else {}
    except Exception as e:
        logger.error('抽取前提条件报错')
        logger.error(str(e) + traceback.format_exc())
        items2 = {}

    try:
        items3 = extract_management_condition(requirement, model_dir) if requirement else {}
    except Exception as e:
        logger.error('抽取管理要求报错')
        logger.error(e)
        items3 = {}

    for items in [items1, items2, items3]:
        return_items['high'].extend(items.get('high', []))
        return_items['mid'].extend(items.get('mid', []))
        return_items['low'].extend(items.get('low', []))

    return return_items

def classify_extract(sentence, part, url):
    data = {
            'use_rule':1,
            'category':1,
            'text':part,
            'app_id':1
    }

    requests.post(url,part)
    return cc.classify_single(text_dict, item_info)[0], cc.classify_single(text_dict, item_info)[1]