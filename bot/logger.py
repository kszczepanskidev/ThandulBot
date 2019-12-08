import logging
import logging.handlers
from os import environ
from datetime import datetime

def start_logger():

    log_formatter = logging.Formatter(logging.BASIC_FORMAT)

    # Logging handler for logfile.
    file_handler = logging.handlers.WatchedFileHandler(environ.get('LOGFILE', '{}.log'.format(datetime.today().strftime('%d-%m-%Y'))))
    file_handler.setFormatter(log_formatter)

    # Logging handler for system output.
    system_handler = logging.StreamHandler()
    system_handler.setFormatter(log_formatter)

    root = logging.getLogger()
    root.setLevel(environ.get('LOGLEVEL', 'INFO'))
    root.addHandler(file_handler)
    root.addHandler(system_handler)