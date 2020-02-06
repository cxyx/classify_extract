# coding: utf-8
import sys

from classify_extract.app.online.server import Server
from classify_extract.conf import conf


def start():
    output_dir = 'classify_extract/output'
    tmp_dir = 'classify_extract/tmp'
    upload_dir = 'classify_extract/upload'
    port = conf.RECV_PORT
    model_links_dir = 'model'
    config_links_dir = 'config'
    if len(sys.argv) >= 3:
        model_links_dir = sys.argv[1]
        config_links_dir = sys.argv[2]
    server = Server(output_dir, tmp_dir, upload_dir, port, model_links_dir, config_links_dir)
    server.start()


if __name__ == '__main__':
    start()
