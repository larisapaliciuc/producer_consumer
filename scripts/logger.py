import os
import sys
import logging

from logging.handlers import RotatingFileHandler


def get_logger(log_name, logs_directory_path, log_max_size=1024):
    log_file_info = os.path.join(logs_directory_path, f'{log_name}.info')
    log_file_warning = os.path.join(logs_directory_path, f'{log_name}.warn')
    log_file_error = os.path.join(logs_directory_path, f'{log_name}.err')

    log_formatter = logging.Formatter(
        '%(asctime)-19s [%(filename)s:%(lineno)s - %(funcName)s() ] [%(levelname)-s] %(message)s')

    log = logging.getLogger(log_name)
    log.setLevel(logging.DEBUG)

    # stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)
    log.addHandler(stream_handler)

    # info
    handler = RotatingFileHandler(log_file_info, maxBytes=log_max_size, backupCount=3)
    handler.setFormatter(log_formatter)
    handler.setLevel(logging.INFO)
    log.addHandler(handler)

    # warn
    handler = RotatingFileHandler(log_file_warning, maxBytes=log_max_size, backupCount=3)
    handler.setFormatter(log_formatter)
    handler.setLevel(logging.WARN)
    log.addHandler(handler)

    # error
    handler = RotatingFileHandler(log_file_error, maxBytes=log_max_size, backupCount=3)
    handler.setFormatter(log_formatter)
    handler.setLevel(logging.ERROR)
    log.addHandler(handler)

    return log
