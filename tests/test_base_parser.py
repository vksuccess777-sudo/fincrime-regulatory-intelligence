from pathlib import Path

import pytest

from src.processing.base_parser import BaseParser
from src.processing.parser_result import ParserResult


class DummyParser(BaseParser):

    @property
    def parser_name(self) -> str:
        return "DummyParser"

    @property
    def parser_version(self) -> str:
        return "1.0"

    def parse(
        self,
        document_id: str,
        file_path: Path,
    ) -> ParserResult:

        return ParserResult(
            document_id=document_id,
            local_path=file_path,
            parser_name=self.parser_name,
            parser_version=self.parser_version,
            page_count=1,
            extracted_pages=["Dummy Page"],
            success=True,
        )


def test_dummy_parser_properties():

    parser = DummyParser()

    assert parser.parser_name == "DummyParser"
    assert parser.parser_version == "1.0"


def test_dummy_parser_parse():

    parser = DummyParser()

    result = parser.parse(
        "DOC001",
        Path("sample.pdf"),
    )

    assert isinstance(result, ParserResult)
    assert result.document_id == "DOC001"
    assert result.page_count == 1
    assert result.success is True


def test_base_parser_is_abstract():

    with pytest.raises(TypeError):
        BaseParser()