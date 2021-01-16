from ..messages.Message import Message
from platform import python_version

class PythonCollector:

    def __init__(self):
        self.messages = []
        self.name = "python"

    def add_message(self, message, subject="", **options):
        self.messages.append(Message(subject, message, **options))
        return self

    def collect(self):
        return {
            "version": python_version(),
        }