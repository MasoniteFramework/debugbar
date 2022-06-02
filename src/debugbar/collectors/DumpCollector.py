from jinja2 import Template


class DumpCollector:
    def __init__(self, name="Dumps", description="Dumped Data"):
        self.name = name
        self.description = description

        self.application = None

    def set_application(self, application):
        self.application = application
        return self

    def restart(self):
        return self

    def collect(self):
        collection = []
        for dump in self.application.make("dumper").get_serialized_dumps():
            collection.append(dump)
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
        {% for dump in data %}
        <div class="mb-4 p-4">
            <div class="flex items-center mb-2">
                <span class="dump-timestamp inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-purple-100 text-purple-800 mr-2">{{ dump.timestamp }}</span>
                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">{{ dump.filename }} : {{ dump.line }}</span>
                <span class="text-xs font-medium ml-4">in {{ dump.method }}()</span>
            </div>
            <div class="grid gap-y-2 gap-x-1 grid-cols-12 py-2 border-t border-gray-300">
                {% for object_name, object in dump.objects.items() %}
                <span class="text-black self-start text-sm col-span-3 truncate">{{ object_name }}</span>
                <div class="col-span-9 ">
                    <!-- obj value -->
                    <pre class="break-all leading-tight text-xs grow" style="white-space: unset;">
                            <code class="language-python rounded-md">{{ object.value }}</code>
                        </pre>
                    <!-- obj props -->
                    {% if object.properties.public %}
                    <p class="text-gray-500 text-sm mt-2">Public Properties</p>
                    <div class="grid gap-y-2 gap-x-1 grid-cols-12 py-2">
                        {% for prop_name, prop in object.properties.public.items() %}
                        <span class="text-black self-baseline text-sm col-span-3 truncate">{{ prop_name }}</span>
                        <div class="col-span-9">
                            <pre class="break-all leading-tight text-xs grow" style="white-space: unset;">
                                <code class="language-python rounded-md">{{ prop }}</code>
                            </pre>
                        </div>
                        {% endfor %}
                    </div>
                    {% endif %}
                    {% if object.properties.private %}
                    <p class="text-gray-500 text-sm mt-2">Private Properties</p>
                    <div class="grid gap-y-2 gap-x-1 grid-cols-12 py-2">
                        {% for prop_name, prop in object.properties.private.items() %}
                        <span class="text-black self-baseline text-sm col-span-3 truncate">{{ prop_name }}</span>
                        <div class="col-span-9">
                            <pre class="break-all leading-tight text-xs grow" style="white-space: unset;">
                                <code class="language-python rounded-md">{{ prop }}</code>
                            </pre>
                        </div>
                        {% endfor %}
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
        """
