from ..messages.Message import Message
import logging

class LogCollector:

    def __init__(self):
        self.messages = []
        self.name = "logging"

    def add_message(self, message, subject=None, options=None):
        print('rr', options)
        self.messages.append(Message(subject, message, options=options))
        return self

    def start_logging(self, log):
        logger = logging.getLogger(log)
        
        logger.addHandler(LogHandler(self))
        print('added handler')
        return self

    def collect(self):
        collection = {}
        for message in self.messages:
            collection.update({message.subject: message.value})

        return collection

class LogHandler(logging.Handler):

    def __init__(self, collector, level=logging.NOTSET):
        super().__init__(level)
        self.collector = collector

    def handle(self, log):
        self.collector.add_message(log.msg, log.name, options={
            "file": log.filename,
            "time": log.time,
            "lineno": log.lineno,
            "logger_name": log.name,
            "level": log.levelname,
        })