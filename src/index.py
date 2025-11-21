import json

# Importar la configuración 
config = json.load(open("config.json", "r"))

# Importar los modelos
from models.content import Content
from models.document import Document

# Importar utilidades
from utils import verbose_print

# Importar las etapas del procesamiento 
from modules.text_extraction import text_extraction  
from modules.split_contents import split_contents
# from modules.extract_latex import extract_latex  
# from modules.latex_to_natural import latex_to_natural  

def main():
    print("=============================================================")
    print("Utilidad De Conversión de Documentos para Evangelizadores IA")
    print("Creado por Fernando Rivera (https://asterkiwebsite.vercel.app)")
    print("Utiliza --verbose para salida detallada")
    print("=============================================================")
    print("Cargando configuración desde config.json")
    print(f"Configuración cargada: {config}")
    print("=============================================================")
    print("Iniciando Etapa 1: Carga de Documentos de Texto")
    documents: list[Document] = text_extraction(config["data"]["extensions"], config["data"]["documents_path"])
    print(f"Etapa 1 completada. Documentos cargados: {len(documents)}")
    verbose_print(f"  Documents: {documents[0:10]}")
    print("=============================================================")
    print("Iniciando Etapa 2.1: Separación de Contenidos en Capítulos, Secciones y Contenidos")
    documents: list[Document] = split_contents(documents)
    print(f"Etapa 2 completada. Contenidos Encontrados: {len(documents)}")
    verbose_print(f"  Contents: {documents[0:10]}") 
    print("=============================================================")


    # Testing output of split contents
    print("From book", documents[0].name)
    for chapter in documents[0].chapters:
        print(" Chapter:", chapter.name)
        for section in chapter.sections:
            print("  Section:", section.name)
            for content in section.contents:
                print("   Content:", content.content)

    # return; # Desactivar la ejecución de las etapas por ahora 
    #
    # print("Iniciando Etapa 2: Extracción de Contenido LaTeX")
    #
    # print(text_documents[2:3])
    # latex_contents = extract_latex(text_documents[2:3], max_workers=config.get("max_workers", None))
    # print(f"Etapa 2 completada. Documentos con contenido LaTeX extraído: {len(latex_contents)}")
    # latex_list = []
    # for doc_id, content in latex_contents.items():
    #     latex_list.extend(content.get("math", []))
    #     latex_list.extend(content.get("macros", []))
    #
    # # Remove duplicates 
    # latex_list = list(set(latex_list))
    #
    # print("Iniciando Etapa 3: Conversión de LaTeX a Lenguaje Natural")
    # latex_contents = latex_to_natural(latex_list[0:20], 20)
    # print(f"Etapa 3 completada. Documentos con contenido LaTeX extraído: {len(latex_contents)}")

if __name__ == "__main__":
    main()

