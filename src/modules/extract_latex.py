from concurrent.futures import ProcessPoolExecutor, as_completed
from pylatexenc.latexwalker import LatexWalker, LatexMathNode, LatexMacroNode
from models.document import Document

def extract_latex_from_doc(doc: Document) -> tuple:
    """
    Extract LaTeX content from a single document.
    Returns (doc.id, {"math": [...], "macros": [...]})
    """
    walker = LatexWalker(doc.content)
    nodes, pos, length = walker.get_latex_nodes()

    math_expressions = []
    macro_expressions = []

    def walk(node):
        if isinstance(node, LatexMathNode):
            math_content = "".join(
                child.latex_verbatim() for child in getattr(node, "nodelist", [])
            )
            math_expressions.append(math_content)
        elif isinstance(node, LatexMacroNode):
            if node.nodeargd:
                args = "".join(
                    arg.latex_verbatim() for arg in node.nodeargd.argnlist if arg
                )
                macro_expressions.append(f"\\{node.macroname}{args}")
            else:
                macro_expressions.append(f"\\{node.macroname}")
        for child in getattr(node, "nodelist", []) or []:
            walk(child)

    for node in nodes:
        walk(node)

    return doc.id, {"math": math_expressions, "macros": macro_expressions}


def extract_latex(documents: list[Document], max_workers: int = None) -> dict:
    """
    """
    latex_contents = {}

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(extract_latex_from_doc, doc) for doc in documents]
        for future in as_completed(futures):
            doc_id, content = future.result()
            latex_contents[doc_id] = content

    return latex_contents
