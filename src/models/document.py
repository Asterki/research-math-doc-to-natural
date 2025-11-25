import uuid

from models.chapter import Chapter
from models.page import Page
from models.section import Section


class Document:
    def __init__(self, name, path):
        self.id = str(uuid.uuid4())
        self.name = name
        self.path = path

        # Children
        self.chapters: list[Chapter] = []
        self.sections: list[Section] = []

        self.pages: list[Page] = []

    def __repr__(self):
        return f"Document(id={self.id}, name={self.name}, path={self.path}, pages_count={len(self.pages)}, chapters_count={len(self.chapters)})"
