import re
from typing import List, Tuple

from models.chapter import Chapter
from models.document import Document
from models.section import Section

from utils import verbose_print


def split_contents(documents: List[Document]) -> List[Document]:
    """
    Split document pages into chapters and sections (based on # rules) and
    accumulate the textual content for each section into Section.content.
    Rules supported (from your spec):
      - '##' (exactly) -> chapter
      - any header that starts with '#' but NOT '##' -> section/subsection
      - lines that are not headings are treated as text (line breaks are NOT paragraph breaks)
    Implementation notes:
      - We treat blank lines (completely empty) as paragraph separators for nicer spacing,
        but we do NOT treat ordinary line-wrapping as paragraph boundary.
      - Paragraph text is normalized into a single string per section.
      - Pages are assigned to the active section/chapter (Section.pages / Chapter.pages).
      - Orphan content (no chapter/section) is stored in document.orphan_contents (list[str]).
    """

    heading_re = re.compile(r"^(#+)\s*(.*)$")

    def normalize_joined_paragraph(lines: List[str]) -> str:
        """
        Join a list of lines into a normalized paragraph string.
        - Remove leading/trailing whitespace per line.
        - If a line ends with a hyphen (word-split), join without hyphen and without extra space.
        - Otherwise join lines with single spaces.
        - Collapse multiple internal whitespace into single spaces.
        """
        if not lines:
            return ""
        joined_parts: List[str] = []
        for i, raw in enumerate(lines):
            s = raw.strip()
            if not s:
                continue
            if joined_parts and joined_parts[-1].endswith("-"):
                # remove trailing hyphen and join directly
                joined_parts[-1] = joined_parts[-1][:-1] + s
            else:
                joined_parts.append(s)
        # join with spaces and collapse multiple spaces
        text = " ".join(joined_parts)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    for document in documents:
        # ensure container attributes exist
        document.chapters = getattr(document, "chapters", [])
        document.sections = getattr(document, "sections", [])
        document.pages = getattr(document, "pages", [])
        document.orphan_contents = getattr(document, "orphan_contents", [])
        document.orphan_sections = getattr(document, "orphan_sections", [])

        current_chapter: Chapter | None = None
        # stack of (level, Section) to support nested subsections
        section_stack: List[Tuple[int, Section]] = []
        current_section: Section | None = None

        # paragraph buffer persists across page boundaries unless a strong delimiter (heading or blank line) is seen
        paragraph_buffer: List[str] = []

        def flush_paragraph_buffer():
            nonlocal paragraph_buffer, current_section, current_chapter
            if not paragraph_buffer:
                return
            paragraph_text = normalize_joined_paragraph(paragraph_buffer)
            paragraph_buffer = []
            if not paragraph_text:
                return

            if current_section is not None:
                # attach to section.content
                current_section.content = getattr(current_section, "content", "")
                if current_section.content:
                    current_section.content += "\n\n" + paragraph_text
                else:
                    current_section.content = paragraph_text
                verbose_print(
                    f"[Split Contents] Appended paragraph to section '{getattr(current_section, 'name', '')}' in document '{document.name}'"
                )
            elif current_chapter is not None:
                # create or get fallback orphan-section inside chapter
                fallback = None
                for sec in getattr(current_chapter, "sections", []):
                    if getattr(sec, "name", "").startswith("(orphan-section"):
                        fallback = sec
                        break
                if fallback is None:
                    fallback_name = "(orphan-section)"
                    fallback = Section(
                        source_chapter=current_chapter,
                        source_document=document,
                        name=fallback_name,
                    )
                    fallback.pages = getattr(fallback, "pages", [])
                    fallback.content = getattr(fallback, "content", "")
                    current_chapter.sections = getattr(current_chapter, "sections", [])
                    current_chapter.sections.append(fallback)
                    document.sections.append(fallback)
                    verbose_print(
                        f"[Split Contents] Created fallback section for orphan content in chapter '{getattr(current_chapter, 'name', '')}'"
                    )
                # append text to fallback
                fallback.content = getattr(fallback, "content", "")
                if fallback.content:
                    fallback.content += "\n\n" + paragraph_text
                else:
                    fallback.content = paragraph_text
                # also set current_section to fallback so subsequent content goes there
                current_section = fallback
                verbose_print(
                    f"[Split Contents] Added orphan paragraph to fallback in chapter '{getattr(current_chapter, 'name', '')}'"
                )
            else:
                # truly orphan (no chapter/section)
                document.orphan_contents.append(paragraph_text)
                verbose_print(
                    f"[Split Contents] Added orphan paragraph (no chapter/section) in document '{document.name}'"
                )

        # iterate pages in order (assumed document.pages is ordered)
        for page in document.pages:
            # Guard: ensure page has the parent_document attribute and is Page-like
            if not hasattr(page, "content"):
                continue

            lines = page.content.splitlines()
            # page-level flag: if we create a heading inside this page, we will consider that the page belongs
            page_triggered_section = False

            for raw_line in lines:
                # keep line as-is but stripped for heading detection
                line = raw_line.rstrip("\r\n")
                stripped = line.strip()

                # Heading detection
                m = heading_re.match(stripped)
                if m:
                    # flush any pending paragraph before switching context
                    flush_paragraph_buffer()

                    hashes = m.group(1)
                    level = len(hashes)
                    heading_text = m.group(2).strip()

                    if level == 2:
                        # exactly '##' -> Chapter
                        chapter = Chapter(source_document=document, name=heading_text)
                        chapter.sections = getattr(chapter, "sections", [])
                        chapter.pages = getattr(chapter, "pages", [])
                        document.chapters.append(chapter)
                        current_chapter = chapter
                        # reset section stack and current_section
                        section_stack = []
                        current_section = None
                        verbose_print(
                            f"[Split Contents] Created chapter '{heading_text}' in document '{document.name}'"
                        )
                        # page belongs to chapter (but not to any section yet)
                        chapter.pages.append(page)
                        page_triggered_section = True
                    else:
                        # it's a section/subsection (any # but not ##)
                        new_section = Section(
                            source_chapter=current_chapter,
                            source_document=document,
                            name=heading_text,
                        )
                        new_section.pages = getattr(new_section, "pages", [])
                        new_section.content = getattr(new_section, "content", "")

                        # attach to document.sections
                        document.sections.append(new_section)

                        # find parent via section_stack (closest level < current level)
                        parent_index = None
                        for idx in range(len(section_stack) - 1, -1, -1):
                            if section_stack[idx][0] < level:
                                parent_index = idx
                                break

                        if parent_index is not None:
                            parent_section = section_stack[parent_index][1]
                            parent_section.subsections = getattr(
                                parent_section, "subsections", []
                            )
                            parent_section.subsections.append(new_section)
                            verbose_print(
                                f"[Split Contents] Created subsection '{heading_text}' (level {level}) under '{getattr(parent_section, 'name', '')}' in document '{document.name}'"
                            )
                        else:
                            # attach to current_chapter if present; otherwise to document orphan sections
                            if current_chapter is not None:
                                current_chapter.sections = getattr(
                                    current_chapter, "sections", []
                                )
                                current_chapter.sections.append(new_section)
                                verbose_print(
                                    f"[Split Contents] Created section '{heading_text}' (level {level}) in chapter '{getattr(current_chapter, 'name', '')}' in document '{document.name}'"
                                )
                            else:
                                document.orphan_sections.append(new_section)
                                verbose_print(
                                    f"[Split Contents] Created orphan section '{heading_text}' (level {level}) in document '{document.name}'"
                                )

                        # update stack and current_section
                        while section_stack and section_stack[-1][0] >= level:
                            section_stack.pop()
                        section_stack.append((level, new_section))
                        current_section = new_section

                        # assign the current page to this section
                        current_section.pages.append(page)
                        page_triggered_section = True

                    # heading line does not count as paragraph content; continue to next line
                    continue

                # blank line: mark paragraph separation (flush)
                if stripped == "":
                    flush_paragraph_buffer()
                    continue

                # normal line -> buffer (do NOT flush at page end; only on blank line or heading)
                paragraph_buffer.append(line)

            # end of page lines
            # If the page did not create/trigger a section but we have a current_section, ensure page is added to it.
            if not page_triggered_section:
                if current_section is not None:
                    if page not in current_section.pages:
                        current_section.pages.append(page)
                elif current_chapter is not None:
                    # page belongs to chapter pages (but not to any section)
                    if page not in current_chapter.pages:
                        current_chapter.pages.append(page)
                else:
                    # no chapter/section yet -> this page content will end up as orphan when flushed
                    pass
            # DO NOT flush paragraph_buffer here; allow flow across page boundaries

        # finished iterating pages for document -> flush remaining buffered paragraph (end of doc)
        flush_paragraph_buffer()

        verbose_print(
            f"[Split Contents] Finished splitting document '{document.name}'. Chapters: {len(getattr(document, 'chapters', []))}, Sections: {len(getattr(document, 'sections', []))}, Orphan paragraphs: {len(getattr(document, 'orphan_contents', []))}"
        )

    print("[Split Contents] Completed splitting contents for all documents.")
    return documents
