import os 
from typing import List, Tuple

from models.chapter import Chapter
from models.content import Content
from models.document import Document
from models.section import Section

from utils import verbose_print

def split_contents(documents: list[Document]) -> Tuple[list[Document], list[Chapter], list[Section], list[Content]]:
    """
    Etapa 2.1: Cargar documentos y separar su contenido en capítulos, secciones y contenidos.  

    Args: 
        documents list[Document]: Lista de objetos Document cargados previamente. 
    Returns:
        Tuple[list[Chapter], list[Section], list[Content]]: Listas de capítulos, secciones y contenidos extraídos.
    """

    chapters: list[Chapter] = []
    sections: list[Section] = []
    contents: list[Content] = []


    for document in documents:
        current_chapter = Chapter(source_document=document, name="") 
        current_section = Section(source_chapter=current_chapter, source_document=document)
        for page in document.pages:
            page_lines = page.content.split("\n") 
            current_section = None 

            for line in page_lines: 
                if line.startswith("## "): # New Chapter
                    current_chapter = Chapter(source_document=document, name=line[2:].strip())
                   
                    if current_chapter not in chapters:
                        chapters.append(current_chapter)
                        document.chapters.append(current_chapter)
                        verbose_print(f"[Split Contents] Created chapter:  from document: {document.name}")
                
                elif line.startswith("#") and not line.startswith("## "): # New Section
                    
                    current_section = Section(source_chapter=current_chapter, source_document=document, name=line[3:].strip())
                    sections.append(current_section)
                    document.sections.append(current_section) 
                    current_chapter.sections.append(current_section)
                    verbose_print(f"[Split Contents] Created section: in chapter")

                else:
                    # Content
                    if current_section is not None:
                        content = Content(source_section=current_section, source_chapter=current_chapter, source_document=document, content=line, content_type="text")
                        contents.append(content)
                        verbose_print(f"[Split Contents] Added content to section") 

    print(f"[Split Contents] Created {len(chapters)} chapters, {len(sections)} sections, and {len(contents)} contents.")

    return documents, chapters, sections, contents 

