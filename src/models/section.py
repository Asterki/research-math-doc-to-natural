import uuid

from models.page import Page


class Section:
    def __init__(self, source_chapter, source_document, name=""):
        self.id = str(uuid.uuid4())
        self.name = name

        # Parents
        self.source_chapter = source_chapter
        self.source_document = source_document

        self.content = ""

        # Relational data
        self.pages: list[Page] = []

    def __repr__(self):
        return f"Section(id={self.id}, name={self.name}, source_chapter={self.source_chapter}, source_document={self.source_document}), pages_count={len(self.pages)}, content_length={len(self.content)})"
