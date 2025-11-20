import os 
from typing import List, Tuple

from models.chapter import Chapter
from models.content import Content
from models.document import Document
from models.section import Section

from utils import verbose_print

def split_contents(documents: list[Document]) -> Tuple[list[Chapter], list[Section], list[Content]]:
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
        verbose_print(f"[Split Contents] Processing document: {document.name}")

        for page in document.pages:
            verbose_print(f"[Split Contents]  Processing page from document: {document.name}")

            # Simple splitting logic based on headings
            lines = page.content.split("\n")
            current_chapter = None
            current_section = None

            for line in lines:
                line = line.strip()
                if line.startswith("Chapter "):
                    current_chapter = Chapter(title=line, parent_document=document)
                    chapters.append(current_chapter)
                    verbose_print(f"[Split Contents]   Found chapter: {line}")
                elif line.startswith("Section "):
                    current_section = Section(title=line, parent_chapter=current_chapter)
                    sections.append(current_section)
                    verbose_print(f"[Split Contents]    Found section: {line}")
                elif line:
                    content = Content(text=line, parent_section=current_section)
                    contents.append(content)
                    verbose_print(f"[Split Contents]     Found content: {line[:30]}...")

    print(f"[Split Contents] Extracted {len(chapters)} chapters, {len(sections)} sections, and {len(contents)} contents.")

    return chapters, sections, contents 

