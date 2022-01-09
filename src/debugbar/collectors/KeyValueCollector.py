from ..messages.Message import Message
from platform import python_version

class KeyValueCollector:

    def __init__(self, name="", description=""):
        self.messages = []
        self.name = name
        self.description = description

    def add(self, key, value, **options):
        self.messages.append(Message(key, value, **options))
        return self
    
    def restart(self):
        self.messages = []
        return self

    def collect(self):
        collection = []
        for index, message in enumerate(self.messages):
            collection.append({
                "id": f"{index}_{self.name}",
                "name": message.name,
                "value": message.value,
            }
        )

        return {
            'description': self.description,
            'count': len(collection),
            'data': collection,
            'html': self.html(),
        }

    def html(self):
        return """
        <template x-for="object in currentContent.data" :key="object.id">
            <div class="flex flex-1 odd:bg-gray-100">
                <div class="pr-4" x-text="object.name"></div>
                <div x-if="typeof object.value === 'object'" x-text="JSON.stringify(object.value, null, 4)"></div>
                <div x-if="typeof object.value !== 'object'" x-text="object.value"></div>
            </div>
        </template>"""