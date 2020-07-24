from logging import Handler


class MyLogsHandler(Handler):
    def __init__(self, callback):
        Handler.__init__(self)
        self.callback = callback

    def emit(self, record):
        log_entry = self.format(record)
        self.callback(log_entry)