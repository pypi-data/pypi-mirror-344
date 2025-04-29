from pathlib import Path
import pytest
from chercher_plugin_epub import ingest
from chercher import Document


@pytest.fixture
def sample_files():
    samples_dir = Path(__file__).parent / "samples"
    return [file.as_uri() for file in samples_dir.iterdir() if file.is_file()]


def test_valid_file(sample_files):
    for uri in sample_files:
        documents = list(ingest(uri=uri))
        assert documents != []

        for doc in documents:
            assert isinstance(doc, Document)
            assert doc.uri == uri
            assert doc.body != ""


def test_invalid_file(tmp_path):
    p = tmp_path / "test.txt"
    p.write_text("Test")

    uri = p.as_uri()
    documents = list(ingest(uri=uri))
    assert documents == []


def test_missing_file(tmp_path):
    p = tmp_path / "missingno.epub"
    documents = list(ingest(uri=p.as_uri()))
    assert documents == []


def test_invalid_uri():
    uri = "https://www.gutenberg.org/cache/epub/11/pg11-images.html"
    documents = list(ingest(uri=uri))
    assert documents == []
