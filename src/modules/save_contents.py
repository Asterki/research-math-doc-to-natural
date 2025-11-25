import os
from typing import List, Optional

from models.document import Document


# helper: sanitize filename component
def _sanitize_filename_part(name: Optional[str], fallback: str) -> str:
    if not name:
        name = fallback
    # replace path separators and control characters
    invalid = ["/", "\\", "\0", "\n", "\r", "\t", ":", "*", "?", '"', "<", ">", "|"]
    safe = "".join(c if c not in invalid else "_" for c in name)
    # trim and reduce whitespace
    safe = "_".join(safe.strip().split())
    # collapse multiple underscores
    while "__" in safe:
        safe = safe.replace("__", "_")
    return safe or fallback


# helper: ensure unique filepath (append _1, _2 if exists)
def _unique_path(path: str) -> str:
    base, ext = os.path.splitext(path)
    candidate = path
    idx = 1
    while os.path.exists(candidate):
        candidate = f"{base}_{idx}{ext}"
        idx += 1
    return candidate


def save_contents(documents: List[Document], artifacts_path: str) -> None:
    """
    Save the documents with their contents into a folder structure:
      artifacts_path/content_extraction/<document_name>/...
    - per-section files: <chapter>/<section>.txt
    - orphan sections: orphan_sections/<section>.txt
    - orphan contents: orphan_contents.txt
    - full stitched file: full.txt
    """
    root = os.path.join(artifacts_path, "content_extraction")
    os.makedirs(root, exist_ok=True)

    for document in documents:
        doc_dirname = _sanitize_filename_part(
            getattr(document, "name", None), "untitled_document"
        )
        doc_dir = os.path.join(root, doc_dirname)
        os.makedirs(doc_dir, exist_ok=True)

        # -------------------------
        # 1) Orphan contents (paragraphs not in any chapter/section)
        # -------------------------
        orphan_contents = getattr(document, "orphan_contents", [])
        if orphan_contents:
            orphan_file = os.path.join(doc_dir, "orphan_contents.txt")
            orphan_file = _unique_path(orphan_file)
            with open(orphan_file, "w", encoding="utf-8") as f:
                for i, item in enumerate(orphan_contents, start=1):
                    # item may be either str or Content-like
                    if isinstance(item, str):
                        text = item
                    else:
                        text = getattr(item, "content", str(item))
                    f.write(text + "\n\n")
            print(
                f"[Save Contents] Guardadas {len(orphan_contents)} entradas huérfanas en {orphan_file}"
            )

        # -------------------------
        # 2) Orphan sections
        # -------------------------
        orphan_sections = getattr(document, "orphan_sections", [])
        if orphan_sections:
            orphan_dir = os.path.join(doc_dir, "orphan_sections")
            os.makedirs(orphan_dir, exist_ok=True)
            for sec in orphan_sections:
                sec_name = _sanitize_filename_part(
                    getattr(sec, "name", None), f"orphan_section_{sec.id[:8]}"
                )
                sec_path = os.path.join(orphan_dir, f"{sec_name}.txt")
                sec_path = _unique_path(sec_path)
                # get section text: prefer Section.content, else join section.contents if present
                content_text = ""
                if hasattr(sec, "content") and sec.content:
                    content_text = sec.content
                else:
                    # fall back to list of Content objects
                    parts = []
                    for c in getattr(sec, "contents", []):
                        if isinstance(c, str):
                            parts.append(c)
                        else:
                            parts.append(getattr(c, "content", str(c)))
                    content_text = "\n\n".join(parts)
                with open(sec_path, "w", encoding="utf-8") as f:
                    f.write(content_text)
                print(
                    f"[Save Contents] Guardada sección huérfana '{getattr(sec, 'name', '')}' en {sec_path}"
                )

        # -------------------------
        # 3) Chapters and their sections
        # -------------------------
        for chapter in getattr(document, "chapters", []):
            chap_name_safe = _sanitize_filename_part(
                getattr(chapter, "name", None), "untitled_chapter"
            )
            chap_dir = os.path.join(doc_dir, chap_name_safe)
            os.makedirs(chap_dir, exist_ok=True)

            # Save each section inside chapter
            for section in getattr(chapter, "sections", []):
                sec_name_safe = _sanitize_filename_part(
                    getattr(section, "name", None), f"section_{section.id[:8]}"
                )
                sec_path = os.path.join(chap_dir, f"{sec_name_safe}.txt")
                sec_path = _unique_path(sec_path)

                # gather text: prefer Section.content, else join section.contents list
                content_text = ""
                if hasattr(section, "content") and section.content:
                    content_text = section.content
                else:
                    parts = []
                    for c in getattr(section, "contents", []):
                        if isinstance(c, str):
                            parts.append(c)
                        else:
                            parts.append(getattr(c, "content", str(c)))
                    content_text = "\n\n".join(parts)

                with open(sec_path, "w", encoding="utf-8") as f:
                    f.write(content_text)
                print(
                    f"[Save Contents] Guardada sección '{getattr(section, 'name', '')}' del capítulo '{getattr(chapter, 'name', '')}' en {sec_path}"
                )

            # Also, if chapter has pages/content outside any section, try to preserve them:
            # We check for any Section in chapter named "(orphan-section)" and save it as its own file
            for sec in getattr(chapter, "sections", []):
                if getattr(sec, "name", "").startswith("(orphan-section"):
                    sec_name_safe = _sanitize_filename_part(
                        getattr(sec, "name", None), f"orphan_section_{sec.id[:8]}"
                    )
                    sec_path = os.path.join(chap_dir, f"{sec_name_safe}.txt")
                    sec_path = _unique_path(sec_path)
                    content_text = getattr(sec, "content", "")
                    with open(sec_path, "w", encoding="utf-8") as f:
                        f.write(content_text)
                    print(
                        f"[Save Contents] Guardada sección fallback '{getattr(sec, 'name', '')}' en {sec_path}"
                    )

        # -------------------------
        # 4) Full stitched document
        # -------------------------
        full_path = os.path.join(doc_dir, "full.txt")
        full_path = _unique_path(full_path)
        parts: List[str] = []

        # a) orphan contents first
        for item in orphan_contents:
            if isinstance(item, str):
                parts.append(item)
            else:
                parts.append(getattr(item, "content", str(item)))

        # b) orphan sections
        for sec in orphan_sections:
            text = ""
            if hasattr(sec, "content") and sec.content:
                text = sec.content
            else:
                subparts = []
                for c in getattr(sec, "contents", []):
                    if isinstance(c, str):
                        subparts.append(c)
                    else:
                        subparts.append(getattr(c, "content", str(c)))
                text = "\n\n".join(subparts)
            header = f"=== Orphan Section: {getattr(sec, 'name', '')} ==="
            parts.append(header)
            parts.append(text)

        # c) chapters and their sections
        for chapter in getattr(document, "chapters", []):
            chap_header = f"\n\n=== Chapter: {getattr(chapter, 'name', '')} ===\n"
            parts.append(chap_header)
            # iterate sections in order
            for section in getattr(chapter, "sections", []):
                sec_header = f"\n-- Section: {getattr(section, 'name', '')} --\n"
                parts.append(sec_header)
                if hasattr(section, "content") and section.content:
                    parts.append(section.content)
                else:
                    subparts = []
                    for c in getattr(section, "contents", []):
                        if isinstance(c, str):
                            subparts.append(c)
                        else:
                            subparts.append(getattr(c, "content", str(c)))
                    parts.append("\n\n".join(subparts))

        # write full file
        with open(full_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(parts))
        print(f"[Save Contents] Guardado documento completo en {full_path}")

    print("[Save Contents] Guardado de todos los documentos completado.")
