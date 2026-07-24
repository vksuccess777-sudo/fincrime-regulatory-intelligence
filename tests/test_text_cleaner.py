import unicodedata

from src.processing.text_cleaner import TextCleaner


def test_empty_string():

    cleaner = TextCleaner()

    assert cleaner.clean("") == ""


def test_unicode_normalization():

    cleaner = TextCleaner()

    text = "A\u0301"

    expected = unicodedata.normalize("NFC", text)

    assert cleaner.clean(text) == expected


def test_line_endings():

    cleaner = TextCleaner()

    text = "A\r\nB\rC"

    assert cleaner.clean(text) == "A\nB\nC"


def test_trailing_spaces():

    cleaner = TextCleaner()

    text = "ABC   \nDEF    "

    assert cleaner.clean(text) == "ABC\nDEF"


def test_multiple_blank_lines():

    cleaner = TextCleaner()

    text = "A\n\n\n\nB"

    assert cleaner.clean(text) == "A\n\nB"


def test_control_characters_removed():

    cleaner = TextCleaner()

    text = "ABC\x00\x01\x02DEF"

    assert cleaner.clean(text) == "ABCDEF"


def test_tabs_preserved():

    cleaner = TextCleaner()

    text = "A\tB\tC"

    assert cleaner.clean(text) == "A\tB\tC"


def test_newlines_preserved():

    cleaner = TextCleaner()

    text = "A\nB\nC"

    assert cleaner.clean(text) == "A\nB\nC"