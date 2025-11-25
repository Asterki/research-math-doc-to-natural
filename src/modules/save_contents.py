import os

from typing import List

from models.document import Document


def save_contents(documents: List[Document], artifacts_path: str) -> None:
    """
    Save the documents with their contents to files in the artifacts directory.
    Each document will be saved as a separate text file with its contents organized.
    """

    os.makedirs(os.path.join(artifacts_path, "content_extraction"), exist_ok=True)

    for document in documents:
        filename = f"{document.name}_contents.txt"
        filepath = os.path.join(artifacts_path, "content_extraction", filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Document: {document.name}\n")
            f.write("=" * 50 + "\n\n")

            for chapter in getattr(document, "chapters", []):
                f.write(f"Chapter: {chapter.name}\n")
                f.write("-" * 40 + "\n")
                for section in getattr(chapter, "sections", []):
                    f.write(f"  Section: {section.name}\n")
                    for content in getattr(section, "contents", []):
                        f.write(f"    Content:\n{content.content}\n\n")

            # Handle orphan sections
            for orphan_section in getattr(document, "orphan_sections", []):
                f.write(f"Orphan Section: {orphan_section.name}\n")
                for content in getattr(orphan_section, "contents", []):
                    f.write(f"  Content:\n{content.content}\n\n")

            # Handle orphan contents
            if hasattr(document, "orphan_contents"):
                f.write("Orphan Contents:\n")
                for content in document.orphan_contents:
                    f.write(f"  Content:\n{content.content}\n\n")

        print(f"[Save Contents] Saved document contents to {filepath}")
