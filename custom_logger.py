import logging


class MyLogsHandler(logging.Handler):
    def __init__(self, message_callback):
            """Constructor"""
            self.callback = message_callback

    def emit(self, record):
        log_entry = self.format(record)
        self.callback(log_entry)