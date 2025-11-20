import uuid

from models.content import Content
from models.page import Page
from models.section import Section

class Chapter:
    def __init__(self, source_document):
        self.id = str(uuid.uuid4())

        # Parent
        self.source_document = source_document

        # Children
        self.sections: list[Section] = [] 
        self.contents: list[Content] = [] 
        
        self.pages: list[Page] = []

    def __repr__(self):
        return f"Chapter(id={self.id}, source_document={self.source_document}, sections_count={len(self.sections)}, contents_count={len(self.contents)})"

