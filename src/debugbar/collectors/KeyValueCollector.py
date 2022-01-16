from ..messages.Message import Message
from jinja2 import Template


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
        for message in self.messages:
            collection.append(
                {
                    "name": message.name,
                    "value": message.value,
                }
            )
        template = Template(self.html())
        return {
            "description": self.description,
            "count": len(collection),
            "data": collection,
            "html": template.render({"data": collection}),
        }

    def html(self):
        return """
        {% for object in data %}
            <div class="flex flex-1 alternate-gray alternate-white p-4">
                <p class="pr-4">{{ object.name }}</p>
                <pre><code class="language-json">{{ object.value }}</code></pre>
                </div>
            </div>
        {% endfor %}"""
