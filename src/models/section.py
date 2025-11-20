import uuid

from models.chapter import Chapter

class Section:
    def __init__(self, source: Chapter, content: str, contents: list = []):
        self.id = str(uuid.uuid4())
        self.source = source
        self.content = content

    def __repr__(self):
        return f"Section(id={self.id}, source={self.source}, content_length={len(self.content)})"

    def summarize(self) -> str:
        return self.content[:100] + "..." if len(self.content) > 100 else self.content 


