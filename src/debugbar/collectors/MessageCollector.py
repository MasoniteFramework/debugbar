from ..messages.Message import Message

class MessageCollector:

    def __init__(self):
        self.messages = []
        self.name = "messages"

    def add_message(self, message, subject="", **options):
        self.messages.append(Message(subject, message, options=options))
        return self

    def collect(self):
        collection = []
        for message in self.messages:
            collection.append({
                'subject': message.subject,
                'message': message.value,
                'color': message.options.get('color', 'green'),
                'tags': [{
                    'message': 'INFO',
                    'color': 'green',
                }],
            })

        return {
            'description': f"Application Messages",
            'data': collection,   
        }
