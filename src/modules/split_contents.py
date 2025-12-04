import os 
from typing import List, Tuple

from models.chapter import Chapter
from models.content import Content
from models.document import Document
from models.section import Section

from utils import verbose_print

def split_contents(documents: list[Document]) -> list[Document]:
    """
    Etapa 2.1: Cargar documentos y separar su contenido en capítulos, secciones y contenidos.  

    Args: 
        documents list[Document]: Lista de objetos Document cargados previamente. 
    Returns:
        Tuple[list[Chapter], list[Section], list[Content]]: Listas de capítulos, secciones y contenidos extraídos.
    """


    for document in documents:
        chapters = []
        chapter_index = 0

        sections = []
        section_index = 0

        current_chapter = Chapter(source_document=document, name="Orphan Chapter") 
        current_section = Section(source_chapter=current_chapter, source_document=document, name="Orphan Section")

        for page in document.pages:
            page_lines = page.content.split("\n") 

            for line in page_lines: 
                if line.startswith("## "): # New Chapter
                    chapter = Chapter(document, name=line[3:].strip())
                    current_chapter = chapter
                    document.chapters.append(chapter)

                    verbose_print(f"[Split Contents] Created chapter:  from document: {document.name}")
                
                elif line.startswith("#") and not line.startswith("## "): # New Section
                    
                    current_section = Section(source_chapter=current_chapter, source_document=document, name=line[3:].strip())
                    sections.append(current_section)
                    document.sections.append(current_section) 
                    current_chapter.sections.append(current_section)

                    verbose_print(f"[Split Contents] Created section: in chapter")

                else: # Content
                    print(line)
                    if current_section is not None:
                        content = Content(source_section=current_section, source_chapter=current_chapter, source_document=document, content=line, content_type="text")
                        verbose_print(f"[Split Contents] Added content to section") 

                        current_section.contents.append(content) 


    print(f"[Split Contents] Created  contents.")

    return documents 

