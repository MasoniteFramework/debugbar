from jinja2 import Template

from ..messages.Message import Message


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
            collection.append({"name": message.name, "value": message.value})
        template = Template(self.html())
        return {
            "description": "Python Version",
            "data": collection,
            "html": template.render({"data": collection}),
        }

    def html(self):
        return """
        {% for object in data %}
            <div class="flex px-4">
                <div class="pr-4">{{ object.name }}</div>
                <div>{{ object.value }}</div>
            </div>
        {% endfor %}
        """
