import os 
from typing import List

from utils import verbose_print

from models.document import Document


def read_data_dir(document_types: str) -> List[Document]:
    """
    Etapa 1: Cargar documentos de texto desde el directorio especificado. 
    Soporta archivos con extensiones definidas en 'document_types'. 
    Almacena el contenido de los documentos en una lista para procesamiento posterior. 
    """

    text_documents = []

    # Enlistar las carpetas en el directorio de documentos 
    verbose_print(f"Escaneando directorio de documentos: data")
    folders = os.listdir("data") 
    for folder in folders:
        folder_path = os.path.join("data", folder)
        if os.path.isdir(folder_path):
            verbose_print(f"Procesando carpeta: {folder}")
           
            # Enlistar los archivos en la carpeta
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    file_ext = filename.split(".")[-1].lower()
                    # Verificar si el archivo es de un tipo soportado
                    if file_ext in document_types:
                        verbose_print(f"  Procesando archivo: {filename}")

                        # Leer el contenido del archivo de texto 
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            text_documents.append(Document(source=filename, content=content)) 
                    else:
                        verbose_print(f"  Archivo ignorado (tipo no soportado): {filename}")

    return text_documents
