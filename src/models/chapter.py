import uuid

class Chapter:
    def __init__(self, source, content):
        self.id = str(uuid.uuid4())
        self.source = source
        self.content = content

    def __repr__(self):
        return f"Document(source={self.source}, content_length={len(self.content)})"


