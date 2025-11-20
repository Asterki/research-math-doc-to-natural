class Page:
    def __init__(self, parent_document, content):
        self.parent_document = parent_document
        self.content = content

    def __repr__(self):
        return f"DocumentPage(source={self.parent_document}, content_length={len(self.content)})"

    def summarize(self) -> str:
        return self.content[:100] + "..." if len(self.content) > 100 else self.content 

