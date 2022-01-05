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
        for index, message in enumerate(self.messages):
            collection.append({
                "id": f"{index}_{self.name}",
                "name": message.name,
                "value": message.value
            }
        )

        return {
            'description': "Python Version",
            'data': collection,
            'html': self.html(),
        }

    def html(self):
        return """
        <template x-for="object in currentContent.data" :key="object.id">
            <div class="flex px-4">
                <div class="pr-4" x-text="object.name"></div>
                <div x-text="object.value"></div>
            </div>
        </template>
        """