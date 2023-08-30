# to run: .venv/Scripts/python.exe -m pytest -vv  tests/test_preprocessor.py -s
import os
from pathlib import Path

import pytest
import repackage

repackage.up()
from scripts.preprocessor import (
    DOCXPreprocessor,
    PDFPreprocessor,
    add_category,
    add_lines,
    chunk_text,
    create_csv_file_if_not_exist,
    determine_language,
    extract_text_from_docx,
    forward_regexp_search,
    get_files_in_dir,
    remove_attachments,
    remove_page_numbers,
    remove_preambule_before_par,
    remove_preambule_before_point,
    replace_forbidden_chars,
    replace_whitespaces,
    split_on_points,
)


def test_get_files_in_dir():
    directory = str(Path(__file__).parent.parent.joinpath(r"tests/test_files"))
    assert len(get_files_in_dir(directory)) == 4


def test_extract_text_from_docx_1():
    directory = str(
        Path(__file__).parent.parent.joinpath(r"tests/test_files/test_file.docx")
    )
    result = extract_text_from_docx(directory)
    assert result[:25] == "This is a paragraph. This"


def test_extract_text_from_docx_2():
    directory = str(
        Path(__file__).parent.parent.joinpath(r"tests/test_files/test_file.doc")
    )
    result = extract_text_from_docx(directory)
    assert result[:25] == "This is a paragraph. This"


def test_extract_text_from_docx_3():
    directory = str(
        Path(__file__).parent.parent.joinpath(r"tests/test_files/test_file.pdf")
    )
    with pytest.raises(TypeError, match="File must be DOCX or DOC."):
        extract_text_from_docx(directory)


def test_split_on_points_1():
    string = "random string § 2 another random string"
    result = split_on_points(string)
    assert result[0] == "random string another random string"


def test_split_on_points_2():
    string = "random string §2 another random string"
    result = split_on_points(string)
    assert result[0] == "random string another random string"


def test_split_on_points_3():
    string = "random string $3 another random string"
    result = split_on_points(string)
    assert result[0] == "random string another random string"


def test_split_on_points_4():
    string = "random string $ 14 another random string"
    result = split_on_points(string)
    assert result[0] == "random string another random string"


def test_split_on_points_5():
    string = "random string 44. another random string"
    result = split_on_points(string)
    assert result[0] == "random string"


def test_remove_preambule_before_par_1():
    string = "random string § 1 another random string"
    result = remove_preambule_before_par(string)
    assert result == "another random string"


def test_remove_preambule_before_par_2():
    string = "random string §1 another random string"
    result = remove_preambule_before_par(string)
    assert result == "another random string"


def test_remove_preambule_before_par_3():
    string = "random string $ 1 another random string"
    result = remove_preambule_before_par(string)
    assert result == "another random string"


def test_remove_preambule_before_par_4():
    string = "random string $1 another random string"
    result = remove_preambule_before_par(string)
    assert result == "another random string"


def test_remove_preambule_before_par_5():
    string = "random string @ 1 another random string"
    result = remove_preambule_before_par(string)
    assert result == string


def test_remove_attachments():
    string = "random string Załącznik nr 1 another random string"
    result = remove_attachments(string)
    assert result == "random string "


def test_replace_forbidden_chars_1():
    string = "random string; another random string"
    result = replace_forbidden_chars(string)
    assert result == "random string, another random string"


def test_replace_forbidden_chars_2():
    string = "random string $3 another random string"
    result = replace_forbidden_chars(string)
    assert result == "random string S3 another random string"


def test_replace_forbidden_chars_3():
    string = "random string? another; random string"
    result = replace_forbidden_chars(string, replacement_dict={"?": "!", ";": ":"})
    assert result == "random string! another: random string"


def test_replace_forbidden_chars_4():
    string = ["random? string", "another; random", "string"]
    result = replace_forbidden_chars(string, replacement_dict={"?": "!", ";": ":"})
    assert result == ["random! string", "another: random", "string"]


def test_replace_forbidden_chars_5():
    with pytest.raises(TypeError, match="Text must be string or list of strings."):
        replace_forbidden_chars(0)


def test_replace_forbidden_chars_6():
    with pytest.raises(TypeError, match="Text must be string or list of strings."):
        replace_forbidden_chars([0, 1, 2])


def test_replace_forbidden_chars_7():
    with pytest.raises(TypeError, match="Must be a dictionary."):
        replace_forbidden_chars(text="Text", replacement_dict=0)


def test_replace_whitespaces_1():
    string = "random string    another  random   string"
    result = replace_whitespaces(string)
    assert result == "random string another random string"


def test_replace_whitespaces_2():
    string = ["random string    another", "random   string"]
    result = replace_whitespaces(string)
    assert result == ["random string another", "random string"]


def test_replace_whitespaces_3():
    with pytest.raises(TypeError, match="Text must be string of list of strings."):
        replace_whitespaces(0)


def test_forward_regexp_search():
    main_string = "random first string another 3. second random string"
    target_string = "first"
    result = forward_regexp_search(main_string=main_string, target_string=target_string)
    assert result == "string another"


def test_determine_language_1():
    text = "Do 1920 r. koleje na ziemiach niemieckich były przeważnie własnością"
    assert determine_language(text) == "pl"


def test_determine_language_2():
    text = "The company generates about half of its total revenue"
    assert determine_language(text) == "en"


def test_determine_language_3():
    text = "Das Unternehmen ist als Aktiengesellschaft organisiert"
    assert determine_language(text) == "de"


def test_get_raw_text_from_pdf():
    filepath = r"tests/test_files/test_file.pdf"
    p = PDFPreprocessor()
    result = p.get_raw_text_from_pdf(filepath)
    assert result[:25] == "This is a paragraph. This"


def test_get_raw_text_from_tables():
    pass


def test_jsonize_pdf():
    pass


def test_add_lines():
    file_path = "test_table.csv"
    lst = ["random", "string"]
    add_lines(lst, file_path)
    with open("test_table.csv", "r") as f:
        lines = f.readlines()
    assert lines == ["sentences\n", "random\n", "string"]
    os.remove("test_table.csv")


def test_create_csv_file_if_not_exist():
    file_path = "test_table.csv"
    create_csv_file_if_not_exist(file_path)
    with open("test_table.csv", "r") as f:
        lines = f.readlines()
    assert lines == ["sentences\n"]
    os.remove("test_table.csv")


def test_preprocess_docx():
    directory = str(
        Path(__file__).parent.parent.joinpath(
            r"tests/test_files/test_Zarządzenie_file.docx"
        )
    )
    p = DOCXPreprocessor(directory)
    result = p.preprocess()
    assert result == ["This is yet another paragraph. This is a point"]


def test_add_category():
    text = "some random text"
    file_path = r"E:\\documents\\tests\\Pytania na egzamin.docx"
    assert add_category(text, file_path) == "Pytania na egzamin: some random text\n"


def test_remove_page_numbers():
    text = "some random 2 z 3 text"
    assert remove_page_numbers(text) == "some random  text"


def test_remove_preambule_before_point():
    text = "random 1. text"
    assert remove_preambule_before_point(text) == "1. text"


def test_chunk_text():
    text = "I wish I were a bird. Bailey wishes he had a nicer car. I am afraid I have to go. We are buzzing on this espresso. She fed it everyday."
    result = chunk_text(text)
    result_list = [
        "I wish I were a bird. Bailey wishes he had a nicer car. I am afraid I have to go.",
        "Bailey wishes he had a nicer car. I am afraid I have to go. We are buzzing on this espresso.",
        "I am afraid I have to go. We are buzzing on this espresso. She fed it everyday.",
    ]
    assert result == result_list
