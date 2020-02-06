# coding=utf-8

# online参数
RECV_PORT = 8000
PREDICT_ROUTER = '/extract'
PREDICT_PATH_ROUTER = '/extract_with_path'
RELOAD_ROUTER = '/reload'
PREDICT_BY_FIELDS = '/extract_by_fields'

CLASSIFY_PORT =  888 #待定
# offline config
# REDIS_HOST = 'redis'  #todo:shan
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PWD = ''

field_config = {
    #todo:待定,默认的classify extract抽取配置
}

SPLIT_SIGN_DICT = {r'1、': r'\d+、',
                   r'1.': r'\d+\.',
                   r'一、': r'[一二三四卫六七八九十]+、',
                   r'（一）': r'（[一二三四卫六七八九十]+）',
                   r'（一）、': r'（[一二三四卫六七八九十]+）、',
                   r'（1）': r'（[0-9]+）',
                   r'（1）、': r'（[0-9]+）、',
                   r'1）': r'[0-9]+）',
                   r'1）、': r'[0-9]+）、'
                   }

