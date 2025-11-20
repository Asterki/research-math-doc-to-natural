import uuid

from models.content import Content
from models.page import Page

class Section:
    def __init__(self, source_chapter, source_document):
        self.id = str(uuid.uuid4())

        # Parents 
        self.source_chapter = source_chapter
        self.source_document = source_document
        
        # Children
        self.contents: list[Content] = [] 

        # Relational data 
        self.pages: list[Page] = []

    def __repr__(self):
        return f"Section(id={self.id}, source_chapter={self.source_chapter}, contents_count={len(self.contents)})"



