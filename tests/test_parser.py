"""Tests for markdown parser."""


from tpman.ingest.parser import MarkdownParser


def test_parser_exists() -> None:
    parser = MarkdownParser()
    assert parser is not None
