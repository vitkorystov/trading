import logging


class Logger:
    def __init__(self, logger_name):
        self._logger = logging.getLogger(logger_name)
        self._logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)

    @property
    def logger(self):
        return self._logger
