from ..messages.Message import Message
from platform import python_version

class PythonCollector:

    def __init__(self, name="python"):
        self.messages = []
        self.name = name

    def add(self, key, value, **options):
        self.messages.append(Message(key, value, **options))
        return self

    def collect(self):
        collection = []
        for message in self.messages:
            collection.append({
                "name": message.name,
                "value": message.value
            }
        )

        return {
            'description': "Python Version",
            # all the rows in JSON
            'data': collection,
            # the skeleton for one row
            'html': self.html(),
        }

    def html(self):
        """Get the skeleton for one collected row. This skeleton needs to be hydrated
        with a 'row' object."""
        return """
            <div class="flex px-4">
                <div class="pr-4" x-text="row.name"></div>
                <div x-text="row.value"></div>
            </div>
        """