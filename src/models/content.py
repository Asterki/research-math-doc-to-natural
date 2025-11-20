
from models.page import Page


class Content:
    def __init__(self, source_document, source_chapter, source_section, content, content_type):
        # Parents 
        self.source_document = source_document 
        self.source_chapter = source_chapter 
        self.source_section = source_section 

        # Content data
        self.content_type = content_type
        self.content = content 

        # Relational data 
        self.pages: list[Page] = []

    def __repr__(self):
        return f"Content(source_chapter={self.source_chapter}, content_length={len(self.content)})"



