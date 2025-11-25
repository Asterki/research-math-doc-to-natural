import os
import re
from typing import List

from utils import verbose_print
from models.document import Document
from models.page import Page

def text_extraction(document_types: List[str], documents_path: str) -> List[Document]:
    """
    Etapa 1: Cargar documentos de texto desde el directorio especificado.
    Soporta archivos con extensiones definidas en 'document_types'.
    Almacena el contenido de los documentos en una lista para procesamiento posterior.

    Args:
        document_types (List[str]): Lista de extensiones de archivo soportadas (ej. ["txt", "md"]).
        documents_path (str): Ruta al directorio que contiene los documentos.

    Returns:
        List[Document]: Lista de objetos Document con el contenido extraído.
    """

    documents: list[Document] = []
    pages: list[Page] = []

    # List out all of the "Documents"
    for document in os.listdir(documents_path):
        document_path = os.path.join(documents_path, document)
        if not os.path.isdir(document_path):
            continue  # Skip non-folder items

        current_document = Document(name=document, path=document_path)

        # List and sort all of the "Pages" numerically
        page_files = [
            f for f in os.listdir(document_path)
            if f.split(".")[-1] in document_types
        ]

        # Sort pages by the number in the filename (e.g., _page_1)
        page_files.sort(key=lambda x: int(re.search(r'_page_(\d+)', x).group(1)))

        # Create Page objects in order
        for page_file in page_files:
            page_path = os.path.join(document_path, page_file)
            with open(page_path, "r", encoding="utf-8") as file:
                content = file.read()
                current_page = Page(parent_document=current_document, content=content)
                current_document.pages.append(current_page)
                pages.append(current_page)
                verbose_print(f"[Text Extraction] Loaded page: {page_file} from document: {document}")

        documents.append(current_document)

    print(f"[Text Extraction] Loaded {len(documents)} documents with a total of {len(pages)} pages.")

    return documents
