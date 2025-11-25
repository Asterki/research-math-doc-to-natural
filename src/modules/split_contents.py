import re
from typing import List

from models.chapter import Chapter
from models.content import Content
from models.document import Document
from models.section import Section

from utils import verbose_print


def split_contents(documents: List[Document]) -> List[Document]:
    """
    Etapa 2.1: Separar el contenido de cada documento en capítulos, secciones,
    subsecciones y contenidos. Soporta:
      - '##' (exactamente) -> capítulo
      - cualquier encabezado que empiece por '#' pero NO por '##' -> sección/subsección
        (e.g. '#', '###', '####' etc.)
      - líneas que no comienzan por '#' -> contenido (se agrupan en párrafos)
    Manejo de huérfanos:
      - document.orphan_contents: contenido fuera de cualquier capítulo/section
      - if content is inside a chapter but not inside a section, it is placed in
        a synthetic "untitled" section within that chapter (keeps structure sane).
    Returns:
        List[Document]: same list but with chapters/sections/contents attached.
    """

    heading_re = re.compile(r'^(#+)\s*(.*)$')

    for document in documents:
        # Ensure containers exist on Document to avoid attribute errors
        if not hasattr(document, "chapters"):
            document.chapters = []
        if not hasattr(document, "sections"):
            document.sections = []
        # place to keep content that truly has no chapter/section
        document.orphan_contents = getattr(document, "orphan_contents", [])
        document.orphan_sections = getattr(document, "orphan_sections", [])

        current_chapter = None
        # stack of (level, Section) for nested sections/subsections
        section_stack: List[tuple[int, Section]] = []

        # helper to create an "untitled" section inside a chapter for orphaned content within a chapter
        def get_or_create_fallback_section(chap: Chapter) -> Section:
            # search existing fallback
            for sec in getattr(chap, "sections", []):
                if getattr(sec, "name", "").startswith("(orphan-section"):
                    return sec
            # create one
            fallback_name = "(orphan-section)"
            fallback = Section(source_chapter=chap, source_document=document, name=fallback_name)
            # ensure lists exist
            chap.sections = getattr(chap, "sections", [])
            chap.sections.append(fallback)
            document.sections.append(fallback)
            verbose_print(f"[Split Contents] Created fallback section for orphan content in chapter '{getattr(chap, 'name', '')}'")
            return fallback

        # iterate pages in order
        for page in document.pages:
            lines = page.content.splitlines()
            paragraph_buffer: List[str] = []

            def flush_paragraph_buffer():
                nonlocal paragraph_buffer
                if not paragraph_buffer:
                    return
                paragraph_text = "\n".join(paragraph_buffer).strip()
                paragraph_buffer = []
                if not paragraph_text:
                    return

                # Determine where to attach the content:
                if section_stack:
                    target_section = section_stack[-1][1]
                    content = Content(source_section=target_section,
                                      source_chapter=getattr(target_section, "source_chapter", current_chapter),
                                      source_document=document,
                                      content=paragraph_text,
                                      content_type="text")
                    target_section.contents = getattr(target_section, "contents", [])
                    target_section.contents.append(content)
                    verbose_print(f"[Split Contents] Added content to section '{getattr(target_section, 'name', '')}' in document '{document.name}'")
                elif current_chapter is not None:
                    # Create/get a fallback section in the chapter to keep structure consistent
                    fallback = get_or_create_fallback_section(current_chapter)
                    content = Content(source_section=fallback,
                                      source_chapter=current_chapter,
                                      source_document=document,
                                      content=paragraph_text,
                                      content_type="text")
                    fallback.contents = getattr(fallback, "contents", [])
                    fallback.contents.append(content)
                    verbose_print(f"[Split Contents] Added orphan content to fallback section in chapter '{getattr(current_chapter, 'name', '')}' in document '{document.name}'")
                else:
                    # truly orphaned content (no chapter at all)
                    content = Content(source_section=None,
                                      source_chapter=None,
                                      source_document=document,
                                      content=paragraph_text,
                                      content_type="text")
                    document.orphan_contents.append(content)
                    verbose_print(f"[Split Contents] Added orphan content (no chapter/section) in document '{document.name}'")

            for raw_line in lines:
                line = raw_line.rstrip("\r\n")
                stripped = line.strip()

                # empty line -> paragraph break
                if stripped == "":
                    flush_paragraph_buffer()
                    continue

                m = heading_re.match(stripped)
                if m:
                    # it's a heading — flush any paragraph before switching context
                    flush_paragraph_buffer()

                    hashes = m.group(1)
                    level = len(hashes)
                    heading_text = m.group(2).strip()

                    # Chapter: exactly level == 2 (i.e., starts with '##')
                    if level == 2:
                        chapter = Chapter(source_document=document, name=heading_text)
                        chapter.sections = getattr(chapter, "sections", [])
                        document.chapters.append(chapter)
                        current_chapter = chapter
                        # reset section stack when a new chapter starts
                        section_stack = []
                        verbose_print(f"[Split Contents] Created chapter '{heading_text}' in document '{document.name}'")
                    else:
                        # Section / Subsection: any heading starting with '#' but not '##'
                        # level indicates nesting depth; higher => deeper subsection
                        new_section = Section(source_chapter=current_chapter, source_document=document, name=heading_text)
                        new_section.subsections = getattr(new_section, "subsections", [])
                        new_section.contents = getattr(new_section, "contents", [])

                        # Attach to document.sections for quick access
                        document.sections.append(new_section)

                        # Find parent for the new section using the stack:
                        # parent is the closest stack item with level < current level
                        parent_index = None
                        for idx in range(len(section_stack) - 1, -1, -1):
                            if section_stack[idx][0] < level:
                                parent_index = idx
                                break

                        if parent_index is not None:
                            parent_section = section_stack[parent_index][1]
                            parent_section.subsections = getattr(parent_section, "subsections", [])
                            parent_section.subsections.append(new_section)
                            verbose_print(f"[Split Contents] Created subsection '{heading_text}' (level {level}) under section '{getattr(parent_section, 'name', '')}' in document '{document.name}'")
                        else:
                            # No parent found. Attach to current chapter if present, otherwise treat as orphan section at document level
                            if current_chapter is not None:
                                current_chapter.sections = getattr(current_chapter, "sections", [])
                                current_chapter.sections.append(new_section)
                                verbose_print(f"[Split Contents] Created section '{heading_text}' (level {level}) in chapter '{getattr(current_chapter, 'name', '')}' in document '{document.name}'")
                            else:
                                document.orphan_sections.append(new_section)
                                verbose_print(f"[Split Contents] Created orphan section '{heading_text}' (level {level}) in document '{document.name}'")

                        # pop stack entries that are deeper or equal to current level, then push this
                        while section_stack and section_stack[-1][0] >= level:
                            section_stack.pop()
                        section_stack.append((level, new_section))

                else:
                    # Regular content line — buffer it as part of a paragraph
                    paragraph_buffer.append(line)

            # end of page -> flush final paragraph buffer
            flush_paragraph_buffer()

        # finished document
        verbose_print(f"[Split Contents] Finished splitting document '{document.name}'. Chapters: {len(getattr(document, 'chapters', []))}, Sections: {len(getattr(document, 'sections', []))}, Orphan contents: {len(getattr(document, 'orphan_contents', []))}")

    print("[Split Contents] Completed splitting contents for all documents.")
    return documents
