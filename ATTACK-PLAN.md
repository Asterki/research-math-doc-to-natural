# Proyecto de Extracción y Conversión de Documentos Matemáticos
Por Fernando Rivera (Asterki)

# Etapa 0: Recolección de Documentos
Estado: Completado

# Etapa 1: Extracción de texto de los documentos
**Estado:** Parcialmente Automatizado

1. Extracción de texto: Separar las páginas en PDF, convertirlas a imágenes y utilizar un modelo (ej. Nougat) para la extracción de texto y formulas LaTeX. **Estado: Automatizado**
2. Organizar los artefactos resultantes con un indicador de qué libro vienen y de qué página se sacaron. **Estado: Automatizado** 
3. Verificar que los documentos se hayan extraído correctamente. **Estado: No Automatizado 

## Etapa 2: Separación de contenidos
**Estado:** Parcialmente Automatizado

1. Separar y unir los trozos de contenidos a sus respectivas secciones y capítulos, utilizando delimitaciones. Estado: **Parcialmente Automatizado**
2. Clasificar cada trozo de contenido en unidades que caigan en las siguientes categorías: Párrafo, Definición, Teorema, Ejemplo. **Estado: No Automatizado**
3. Separación de contenido en distintas carpetas, del nivel más alto a más bajo: Libro -> Capítulo -> Sección -> Definición/Teorema/Ejemplo/Párrafo. **Estado: No Automatizado**

## Etapa 3: Verificación de LaTeX
**Estado:** Parcialmente Automatizado

1. Separación del LaTex del texto original utilizando expresiones regulares. **Estado: Automatizado**
2. Almacenamiento de las formulas, guardado su respectiva fila, columna, y documento. **Estado: No Automatizado**
3. Comparar las formulas LaTeX contra la fuente original, reportar y solucionar errores en ellas. **Estado: No Automatizado**

## Etapa 4: Conversión de LaTeX a Lenguaje Natural
**Estado:** Parcialmente Automatizado

1. Convertir símbolos simples (ej. $X$, $\pi$, $\infty$) a lenguaje natural (X, pi, infinity) utilizando un diccionario de LaTex -> Inglés básico. No Aplicar si estos símbolos se encuentran dentro de otras formulas más complejas. **Estado: Parcialmente Automatizado**
2. Convertir formulas complicadas a inglés utilizando un (o varios) LLM, al cual se le dará el contexto del documento, para generar traducciones acertadas de acuerdo al contenido. **Estado: Parcialmente Automatizado** 
3. En caso de usar varios LLM, utilizar otro modelo/script/manual el cual "maracará" los resultados que se alejen mucho del resultado de la mayoría. **Estado: No Automatizado** 

## Etapa 5: Reemplazar el LaTeX de los documentos por el Lenguaje Natural
**Estado:** No Automatizado

1. Crear una copia aparte del texto primeramente extraído por Nougat. **Estado: No Automatizado**
2. Utilizando el inicio y fin del latex extraído en la Etapa 3, Paso 2, reemplazar la formula latex con su respectiva representación en inglés. **Estado: No Automatizado**

## Etapa 6: Creación de los documentos JSON
**Estado: No Automatizado**

1. Utilizando los nombres de las carpetas y archivos, los cuales representan el libro, capítulo, y sección, llenar los primeros valores del documento. **Estado: No Automatizado**
2. Reemplazar el texto de cada documento de texto conteniendo las definiciones, ejemplos, etc, que pueda causar problemas dentro de un documento JSON (ej: ", \n, :) con versiones seguras de usar. **Estado: No Automatizado** 

## Etapa 7: Testing
**Estado: Pendiente**

1. Entre cada etapa hay incertidumbres, estudiar qué tan seguido aparecen y probar distintos métodos en caso de ser fallos catastróficos
2. Mejorar la eficiencia del sistema

## Etapa 8: Deployment
**Estado: En Progreso**

1. Hacer una herramienta web la cual dé inicio a todo el proceso (etapa 1-6)
