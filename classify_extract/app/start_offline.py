# coding: utf-8
from classify_extract.app.offline.service import Service
from classify_extract.conf import conf

from classify_extract.app.driver import generate_request_id, logger_offline as logger



def start():
    input_dir = 'classify_extract/input'
    output_dir = 'classify_extract/output'
    conf_dir = 'classify_extract/conf'
    service = Service(input_dir, output_dir, conf_dir, conf.REDIS_HOST, conf.REDIS_PORT, conf.REDIS_DB, conf.REDIS_PWD)

    service.start()


if __name__ == '__main__':
    start()
