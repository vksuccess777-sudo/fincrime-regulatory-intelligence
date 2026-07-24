"""
Text Cleaner

Provides safe text normalization for extracted document text.

Sprint:
    Sprint 5 - D3

Responsibilities
----------------
- Normalize Unicode
- Normalize line endings
- Remove ASCII control characters
- Trim trailing whitespace
- Collapse excessive blank lines

This class intentionally DOES NOT:

- Remove headers
- Remove footers
- Detect sections
- Merge paragraphs
- Chunk text
"""

import re
import unicodedata


class TextCleaner:
    """
    Performs safe normalization of extracted document text.
    """

    def clean(self, text: str) -> str:
        """
        Cleans extracted text while preserving document structure.
        """

        if text == "":
            return ""

        # Unicode normalization
        text = unicodedata.normalize("NFC", text)

        # Normalize Windows/Mac line endings
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Remove ASCII control characters
        # Preserve:
        #   TAB (9)
        #   LF  (10)
        text = "".join(
            ch
            for ch in text
            if (
                ord(ch) >= 32
                or ch in ("\n", "\t")
            )
        )

        # Remove trailing whitespace
        lines = [line.rstrip() for line in text.split("\n")]

        text = "\n".join(lines)

        # Collapse 3+ blank lines into 2
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()