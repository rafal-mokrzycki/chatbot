# to run: .venv/Scripts/python.exe -m pytest -vv  tests/test_preprocessor.py -s
import os
from pathlib import Path

import repackage

repackage.up()
from scripts.preprocessor import (
    DOCXPreprocessor,
    add_lines,
    create_csv_file_if_not_exist,
    extract_text_from_docx,
    forward_regexp_search,
    get_files_in_dir,
    remove_attachments,
    remove_preambule,
    replace_forbidden_chars,
    replace_whitespaces,
    split_on_points,
)


def test_get_files_in_dir():
    directory = str(Path(__file__).parent.parent.joinpath(r"tests/test_files"))
    assert len(get_files_in_dir(directory)) == 3


def test_extract_text_from_docx():
    directory = str(
        Path(__file__).parent.parent.joinpath(r"tests/test_files/test_file.docx")
    )
    result = extract_text_from_docx(directory)
    assert result[:25] == "This is a paragraph. This"


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


def test_remove_preambule_1():
    string = "random string § 1 another random string"
    result = remove_preambule(string)
    assert result == "another random string"


def test_remove_preambule_2():
    string = "random string §1 another random string"
    result = remove_preambule(string)
    assert result == "another random string"


def test_remove_preambule_3():
    string = "random string $ 1 another random string"
    result = remove_preambule(string)
    assert result == "another random string"


def test_remove_preambule_4():
    string = "random string $1 another random string"
    result = remove_preambule(string)
    assert result == "another random string"


def test_remove_preambule_5():
    string = "random string @ 1 another random string"
    result = remove_preambule(string)
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
    string = "random string; another random string"
    result = replace_forbidden_chars(string, replace_with="!")
    assert result == "random string! another random string"


def test_replace_forbidden_chars_3():
    string = "random string? another; random string"
    result = replace_forbidden_chars(string, forbidden_chars=["?", ";"])
    assert result == "random string, another, random string"


def test_replace_whitespaces():
    string = "random string    another  random   string"
    result = replace_whitespaces(string)
    assert result == "random string another random string"


def test_forward_regexp_search():
    main_string = "random first string another 3. second random string"
    target_string = "first"
    result = forward_regexp_search(main_string=main_string, target_string=target_string)
    assert result == "string another"


def test_get_raw_text_from_pdf():
    pass


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
