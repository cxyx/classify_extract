# coding=utf-8
import uuid

from dg_logging.dg_logging import DGLogger

logger_online = DGLogger.Builder().set_name('offline_logger').set_propagate(False).set_log_file_path(
    'classify_extract/log/classify_extract_online.log').build()
logger_offline = DGLogger.Builder().set_name('online_logger').set_propagate(False).set_log_file_path(
    'classify_extract/log/classify_extract_offline.log').build()

logger_processor = logger_online
logger_server = logger_online


def generate_request_id():
    return uuid.uuid4()
