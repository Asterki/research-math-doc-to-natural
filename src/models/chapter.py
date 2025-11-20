import uuid

from models.page import Page 

class Chapter:
    def __init__(self, source: Page, content: str, sections: list = []):
        self.id = str(uuid.uuid4())
        self.source = source
        self.content = content
        self.sections = sections

    def __repr__(self):
        return f"Chapter(id={self.id}, source={self.source}, content_length={len(self.content)}, sections_count={len(self.sections)})"

    def summarize(self) -> str:
        return self.content[:100] + "..." if len(self.content) > 100 else self.content 

