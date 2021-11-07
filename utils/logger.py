import os
import logging
from logging.handlers import RotatingFileHandler


def get_logger(log_name, logs_directory_path, log_max_size=1024):
    log_file_warning = os.path.join(logs_directory_path, f'{log_name}.warn'),
    log_file_error = os.path.join(logs_directory_path, f'{log_name}.err')

    log_formatter = logging.Formatter(
        '%(asctime)-19s [%(filename)s:%(lineno)s - %(funcName)20s() ] [%(levelname)-8s] %(message)s')

    log = logging.getLogger(log_name)
    log.setLevel(logging.INFO)

    # stdout
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    stream_handler.setLevel(logging.DEBUG)
    log.addHandler(stream_handler)

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
