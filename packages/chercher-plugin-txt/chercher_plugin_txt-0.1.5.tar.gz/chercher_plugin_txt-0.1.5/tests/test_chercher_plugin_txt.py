from chercher_plugin_txt import ingest
from chercher import Document

CONTENT = "Hello, world"


def test_valid_file_with_file_uri(tmp_path):
    p = tmp_path / "test.txt"
    p.write_text(CONTENT)

    uri = p.as_uri()
    documents = list(ingest(uri=uri))
    assert len(documents) == 1
    for doc in documents:
        assert isinstance(doc, Document)
        assert doc.uri == uri
        assert doc.title == p.stem
        assert doc.body == CONTENT
        assert doc.hash is not None


def test_valid_file_with_relative_uri(tmp_path):
    p = tmp_path / "test.txt"
    p.write_text(CONTENT)

    uri = p.as_posix()
    documents = list(ingest(uri=uri))
    assert len(documents) == 1
    for doc in documents:
        assert isinstance(doc, Document)
        assert doc.uri == p.as_uri()
        assert doc.title == p.stem
        assert doc.body == CONTENT
        assert doc.hash is not None


def test_invalid_file(tmp_path):
    p = tmp_path / "test.md"
    p.write_text(CONTENT)

    uri = p.as_uri()
    documents = list(ingest(uri=uri))
    assert documents == []


def test_missing_file(tmp_path):
    p = tmp_path / "missingno.txt"
    documents = list(ingest(uri=p.as_uri()))
    assert documents == []


def test_invalid_uri():
    uri = "https://files/file.txt"
    documents = list(ingest(uri=uri))
    assert documents == []
