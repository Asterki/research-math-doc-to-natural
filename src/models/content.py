import uuid

from models.section import Section

class Chapter:
    def __init__(self, source: Section, type = "paragraph", content: str):
        self.id = str(uuid.uuid4())
        self.source = source 
        self.type = type 
        self.content = content

    def __repr__(self):
        return f"Chapter(id={self.id}, source={self.source}, content_length={len(self.content)})"

    def summarize(self) -> str:
        return self.content[:100] + "..." if len(self.content) > 100 else self.content 


