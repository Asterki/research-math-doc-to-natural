import os 
from typing import List, Tuple

from utils import verbose_print

from models.document import Document
from models.page import Page 

def text_extraction(document_types: List[str], documents_path: str) -> Tuple[List[Document], List[Page]]:
    """
    Etapa 1: Cargar documentos de texto desde el directorio especificado.
    Soporta archivos con extensiones definidas en 'document_types'.
    Almacena el contenido de los documentos en una lista para procesamiento posterior.

    Args: 
        document_types (str): Lista de extensiones de archivo soportadas (ej. ["txt", "md"]).
        documents_path (str): Ruta al directorio que contiene los documentos.
    Returns:
        List[Document]: Lista de objetos Document con el contenido extraído.
    """

    documents: list[Document] = []
    pages: list[Page] = []

    # Parent folders: "Documents"
    # Child items: "Pages"

    # List out all of the "Documents"
    for document in os.listdir(documents_path):
        current_document = Document(name=document, path=os.path.join(documents_path, document))

        # List out all of the "Pages"
        for page in os.listdir(os.path.join(documents_path, document)):
            # Check if they are of a supported type
            page_extension = page.split(".")[-1]
            if page_extension in document_types:

                # Create the pages and add them to the document
                with open(os.path.join(documents_path, document, page), "r", encoding="utf-8") as file:
                    content = file.read()
                    current_page = Page(parent_document=current_document, content=content)
                    current_document.pages.append(current_page)
                    pages.append(current_page)
                    verbose_print(f"[Text Extraction] Loaded page: {page} from document: {document}") 

        documents.append(current_document)

    print(f"[Text Extraction] Loaded {len(documents)} documents with a total of {len(pages)} pages.") 

    return documents, pages 
