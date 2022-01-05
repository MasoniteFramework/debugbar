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
            'data': collection,   
        }
    
    def html(self):
        return """
            <template x-for="(object, index) in currentContent">
                <div class="flex px-4">
                    <div class="pr-4" x-text="object.name"></div>
                    <div x-text="object.value"></div>
                </div>
            </template>
        """