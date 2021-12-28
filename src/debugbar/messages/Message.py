class Message:

    def __init__(self, subject, value, options={}):
        self.subject = subject
        self.value = value
        self.options = options