from pyexpat.errors import messages
from ..messages.Message import Message
from jinja2 import Template


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
        for message in self.messages:
            collection.append(
                {
                    "name": message.name,
                    "message": message.value,
                    "color": message.options.get("color", "green"),
                    "tags": message.tags,
                }
            )
        # render data to html
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
            <div class="flex justify-between alternate-gray alternate-white p-4">
                <p class="text-{{ object.color }}-700">{{ object.message }}</p>
                {% for tag in object.tags %}
                    <div>
                        <span class="inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white rounded bg-{{ tag.color }}-700">{{ tag.message }}</span>
                    </div>
                {% endfor %}
            </div>
        {% endfor %}
        """
