from ..messages.Message import Message

class MessageCollector:

    def __init__(self, name="Messages", description="Application Messages"):
        self.messages = []
        self.name = name
        self.description = description

    def add_message(self, message, subject="", **options):
        self.messages.append(Message(subject, message, options=options))
        return self

    def restart(self):
        self.messages = []
        return self

    def collect(self):
        collection = []
        for index, message in enumerate(self.messages):
            collection.append({
                "id": f"{index}_{self.name}",
                'name': message.name,
                'message': message.value,
                'color': message.options.get('color', 'green'),
                'tags': [{
                    'message': 'INFO',
                    'color': 'green',
                }],
            })

        return {
            'description': self.description,
            'count': len(collection),
            'data': collection,
            "html": self.html(),
        }

    def html(self):
        return """
        <template x-for="object in currentContent.data" :key="object.id">
            <div class="flex justify-between px-4 odd:bg-gray-100">
                <div x-text="object.message" :class="'text-'+object.color+'-700'"></div>
                <template x-for="tag in object.tags">
                    <div>
                        <span class="inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white  rounded" :class="'bg-'+tag.color+'-700'" x-text="tag.message"></span>
                    </div>
                </template>
            </div>
        </template>
        """