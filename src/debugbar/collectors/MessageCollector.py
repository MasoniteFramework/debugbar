from ..messages.Message import Message

class MessageCollector:

    def __init__(self):
        self.messages = []
        self.name = "messages"

    def add_message(self, message, subject="", **options):
        self.messages.append(Message(subject, message, **options))
        return self

    def collect(self):
        collection = {}
        for message in self.messages:
            collection.update({message.subject: message.value})

        return collection
