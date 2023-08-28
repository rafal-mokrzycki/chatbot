# to run: .venv/Scripts/python.exe -m pytest -vv  tests/test_preprocessor.py -s
import os
import tempfile
from pathlib import Path

import repackage

repackage.up()
from scripts.preprocessor import (
    DOCXPreprocessor,
    PDFPreprocessor,
    Preprocessor,
    TableHandler,
)


def test_search_files_in_dir():
    directory = r"tests/test_files"
    filepath = r"tests/test_files/tmp.pdf"
    os.mkdir(directory)
    with open(filepath, "a"):
        pass
    p = Preprocessor(directory)
    assert len(p.search_files_in_dir(directory)) == 1
    os.remove(filepath)
    os.rmdir(directory)


def test_extract_sentences_from_docx():
    pass


def test_preprocess_docx():
    pass


def test_remove_attachments():
    pass


def test_remove_preambule():
    pass


def test_replace_forbidden_chars():
    pass


def test_replace_whitespaces():
    pass


def test_split_on_points():
    pass


def test_forward_regexp_search():
    pass


def test_get_raw_text_from_pdf():
    pass


def test_get_raw_text_from_tables():
    pass


def test_jsonize_pdf():
    pass


def test_add_lines():
    pass


fp = tempfile.TemporaryFile()
fp.close()
temp_dir = tempfile.TemporaryDirectory()
print(temp_dir.name)
# use temp_dir, and when done:
temp_dir.cleanup()
