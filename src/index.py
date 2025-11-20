import json

# Importar la configuración 
config = json.load(open("config.json", "r"))

from utils import verbose_print

# Importar las stages 
from modules.read_data_dir import read_data_dir  
from modules.extract_latex import extract_latex  
from modules.latex_to_natural import latex_to_natural  

def main():
    print("=============================================================")
    print("Utilidad De Conversión de Documentos para Evangelizadores IA")
    print("Creado por Fernando Rivera (https://asterkiwebsite.vercel.app)")
    print("Utiliza --verbose para salida detallada")
    print("=============================================================")
    print("\n")

    print("Cargando configuración desde config.json")
    verbose_print(f"Configuración cargada: {config}")

    print("Iniciando Etapa 0: Extracción de texto de los documentos")

    return; # Desactivar la ejecución de las etapas por ahora 

    print("Iniciando Etapa 1: Carga de Documentos de Texto")
    text_documents = read_data_dir(config["data"]["extensions"])
    print(f"Etapa 1 completada. Documentos cargados: {len(text_documents)}")

    print("Iniciando Etapa 2: Extracción de Contenido LaTeX")

    print(text_documents[2:3])
    latex_contents = extract_latex(text_documents[2:3], max_workers=config.get("max_workers", None))
    print(f"Etapa 2 completada. Documentos con contenido LaTeX extraído: {len(latex_contents)}")
    latex_list = []
    for doc_id, content in latex_contents.items():
        latex_list.extend(content.get("math", []))
        latex_list.extend(content.get("macros", []))

    # Remove duplicates 
    latex_list = list(set(latex_list))
    
    print("Iniciando Etapa 3: Conversión de LaTeX a Lenguaje Natural")
    latex_contents = latex_to_natural(latex_list[0:20], 20)
    print(f"Etapa 3 completada. Documentos con contenido LaTeX extraído: {len(latex_contents)}")

if __name__ == "__main__":
    main()

