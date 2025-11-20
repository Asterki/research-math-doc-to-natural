

from models.document import Document


class Page:
    def __init__(self, source: Document, content):
        self.source = source
        self.content = content

    def __repr__(self):
        return f"DocumentPage(source={self.source}, content_length={len(self.content)})"

    def summarize(self) -> str:
        return self.content[:100] + "..." if len(self.content) > 100 else self.content 

