class Message:
    def __init__(self, name, value, options={}):
        self.name = name
        self.value = value
        self.options = options
        self.tags = []
        if options.get('tags'):
            self.tags.append(options.get('tags'))
