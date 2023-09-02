# to run: .venv/Scripts/python.exe -m pytest -vv  tests/test_parser.py -s
import os
from pathlib import Path

import aspose.pdf as pdf
import pytest
import repackage

repackage.up()
from scripts import parser


def test_get_files_in_dir():
    directory = str(Path(__file__).parent.parent.joinpath(r"tests/test_files"))
    assert len(parser.get_files_in_dir(directory)) == 6


def test_extract_text_from_docx_1():
    directory = str(
        Path(__file__).parent.parent.joinpath(r"tests/test_files/test_file.docx")
    )
    result = parser.extract_text_from_docx(directory)
    assert result[:25] == "This is a paragraph. This"


def test_extract_text_from_docx_2():
    directory = str(
        Path(__file__).parent.parent.joinpath(r"tests/test_files/test_file.doc")
    )
    result = parser.extract_text_from_docx(directory)
    assert result[:25] == "This is a paragraph. This"


def test_extract_text_from_docx_3():
    directory = str(
        Path(__file__).parent.parent.joinpath(r"tests/test_files/test_file.pdf")
    )
    with pytest.raises(TypeError, match="File must be DOCX or DOC."):
        parser.extract_text_from_docx(directory)


def test_split_on_points_1():
    string = "random string § 2 another random string"
    result = parser.split_on_points(string)
    assert result[0] == "random string another random string"


def test_split_on_points_2():
    string = "random string §2 another random string"
    result = parser.split_on_points(string)
    assert result[0] == "random string another random string"


def test_split_on_points_3():
    string = "random string $3 another random string"
    result = parser.split_on_points(string)
    assert result[0] == "random string another random string"


def test_split_on_points_4():
    string = "random string $ 14 another random string"
    result = parser.split_on_points(string)
    assert result[0] == "random string another random string"


def test_split_on_points_5():
    string = "random string 44. another random string"
    result = parser.split_on_points(string)
    assert result[0] == "random string"


def test_remove_preambule_before_par_1():
    string = "random string § 1 another random string"
    result = parser.remove_preambule_before_par(string)
    assert result == "another random string"


def test_remove_preambule_before_par_2():
    string = "random string §1 another random string"
    result = parser.remove_preambule_before_par(string)
    assert result == "another random string"


def test_remove_preambule_before_par_3():
    string = "random string $ 1 another random string"
    result = parser.remove_preambule_before_par(string)
    assert result == "another random string"


def test_remove_preambule_before_par_4():
    string = "random string $1 another random string"
    result = parser.remove_preambule_before_par(string)
    assert result == "another random string"


def test_remove_preambule_before_par_5():
    string = "random string @ 1 another random string"
    result = parser.remove_preambule_before_par(string)
    assert result == string


def test_remove_attachments():
    string = "random string Załącznik nr 1 another random string"
    result = parser.remove_attachments(string)
    assert result == "random string"


def test_replace_forbidden_chars_1():
    string = "random string; another random string"
    result = parser.replace_forbidden_chars(string)
    assert result == "random string, another random string"


def test_replace_forbidden_chars_2():
    string = "random string $3 another random string"
    result = parser.replace_forbidden_chars(string)
    assert result == "random string S3 another random string"


def test_replace_forbidden_chars_3():
    string = "random string? another; random string"
    result = parser.replace_forbidden_chars(string, replacement_dict={"?": "!", ";": ":"})
    assert result == "random string! another: random string"


def test_replace_forbidden_chars_4():
    string = ["random? string", "another; random", "string"]
    result = parser.replace_forbidden_chars(string, replacement_dict={"?": "!", ";": ":"})
    assert result == ["random! string", "another: random", "string"]


def test_replace_forbidden_chars_5():
    with pytest.raises(TypeError, match="Text must be string or list of strings."):
        parser.replace_forbidden_chars(0)


def test_replace_forbidden_chars_6():
    with pytest.raises(TypeError, match="Text must be string or list of strings."):
        parser.replace_forbidden_chars([0, 1, 2])


def test_replace_forbidden_chars_7():
    with pytest.raises(TypeError, match="Must be a dictionary."):
        parser.replace_forbidden_chars(text="Text", replacement_dict=0)


def test_replace_whitespaces_1():
    string = "random string    another  random   string"
    result = parser.replace_whitespaces(string)
    assert result == "random string another random string"


def test_replace_whitespaces_2():
    string = ["random string    another", "random   string"]
    result = parser.replace_whitespaces(string)
    assert result == ["random string another", "random string"]


def test_replace_whitespaces_3():
    with pytest.raises(TypeError, match="Text must be string of list of strings."):
        parser.replace_whitespaces(0)


def test_forward_regexp_search():
    main_string = "random first string another 3. second random string"
    target_string = "first"
    result = parser.forward_regexp_search(
        main_string=main_string, target_string=target_string
    )
    assert result == "string another"


def test_determine_language_1():
    text = "Do 1920 r. koleje na ziemiach niemieckich były przeważnie własnością"
    assert parser.determine_language(text) == "pl"


def test_determine_language_2():
    text = "The company generates about half of its total revenue"
    assert parser.determine_language(text) == "en"


def test_determine_language_3():
    text = "Das Unternehmen ist als Aktiengesellschaft organisiert"
    assert parser.determine_language(text) == "de"


def test_extract_text_from_pdf():
    filepath = r"tests/test_files/test_table_file.pdf"
    result = parser.extract_text_from_pdf(filepath)
    assert result == "Text1 Text2 Obj2 Obj33 Obj1 Obj22"


# test_extract_text_from_pdf()


def test_remove_keywords_1():
    text = "This is a sample text."
    to_remove = ["sample", "a"]
    assert parser.remove_keywords(text, to_remove) == "This is text."


def test_remove_keywords_2():
    text = "This is a sample text Przedmiotowy."
    assert parser.remove_keywords(text) == "This is a sample text ."


def test_remove_codes():
    text = "This K_K1 is a EP-22 sample K_12 text."
    assert parser.remove_codes(text) == "This is a sample text."


def test_add_lines():
    file_path = "test_table.csv"
    lst = ["random", "string"]
    parser.add_lines(lst, file_path)
    with open("test_table.csv", "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert lines == ["sentences\n", "random\n", "string"]
    os.remove("test_table.csv")


def test_create_csv_file_if_not_exist():
    file_path = "test_table.csv"
    parser.create_csv_file_if_not_exist(file_path)
    with open("test_table.csv", "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert lines == ["sentences\n"]
    os.remove("test_table.csv")


def test_parse_docx():
    directory = str(
        Path(__file__).parent.parent.joinpath(
            r"tests/test_files/test_Zarządzenie_file.docx"
        )
    )
    p = parser.DOCXParser(directory)
    result = p.parse()
    assert result == ["This is yet another paragraph. This is a point"]


def test_add_category():
    text = "some random text"
    file_path = r"E:\\documents\\tests\\Pytania na egzamin.docx"
    assert parser.add_category(text, file_path) == "Pytania na egzamin: some random text"


def test_remove_page_numbers():
    text = "some random 2 z 3 text"
    assert parser.remove_page_numbers(text) == "some random  text"


def test_remove_preambule_before_point():
    text = "random 1. text"
    assert parser.remove_preambule_before_point(text) == "1. text"


def test_chunk_text():
    text = "I wish I were a bird. Bailey wishes he had a nicer car. I am afraid I have to go. We are buzzing on this espresso. She fed it everyday."
    result = parser.chunk_text(text)
    result_list = [
        "I wish I were a bird. Bailey wishes he had a nicer car. I am afraid I have to go.",
        "Bailey wishes he had a nicer car. I am afraid I have to go. We are buzzing on this espresso.",
        "I am afraid I have to go. We are buzzing on this espresso. She fed it everyday.",
    ]
    assert result == result_list


def test_get_header_1():
    text = "Sylabus Wydziału Ekonomii i Zarządzania Uczelni Łazarskiego Finanse i rachunkowość, profil praktyczny 1."
    file_path = r"test-path/Sylabus_praktyka_zawodowa_FiR-I-nst.pdf"
    assert (
        parser.get_header(text, file_path)
        == "Sylabus Wydziału Ekonomii i Zarządzania Uczelni Łazarskiego Finanse i rachunkowość, profil praktyczny"
    )


def test_get_header_2():
    text = "some random text"
    file_path = r"test-path/Sylabus_praktyka_zawodowa_FiR-I-nst.pdf"
    assert (
        parser.get_header(text, file_path)
        == "Sylabus praktyk zawodowych na kierunku Finanse i Rachunkowość"
    )


def test_get_header_3():
    text = "Sylabus Wydziału Ekonomii i Zarządzania Uczelni Łazarskiego Finanse i rachunkowość, profil praktyczny"
    file_path = r"test-path/Sylabus_praktyka_zawodowa_Z-I-nst.pdf"
    assert (
        parser.get_header(text, file_path)
        == "Sylabus praktyk zawodowych na kierunku Zarządzanie"
    )


def test_get_header_4():
    text = "Sylabus Wydziału Ekonomii i Zarządzania Uczelni Łazarskiego Finanse i rachunkowość, profil praktyczny"
    file_path = r"test-path/Sylabus_praktyka_zawodowa_Ekonomia-I-nst.pdf"
    assert (
        parser.get_header(text, file_path)
        == "Sylabus praktyk zawodowych na kierunku Ekonomia"
    )


def test_prettify_json():
    json = {"Nazwa przedmiotu": "praktyka"}
    header = "random text Zarządzanie random text"
    assert parser.prettify_json(json, header) == [
        "Nazwa przedmiotu przedmiotu praktyka zawodowa na kierunku Zarządzanie: praktyka"
    ]


def test_extract_text_from_textual_pdf():
    file_path = r"tests/test_files/test_file.pdf"
    assert (
        parser.extract_text_from_textual_pdf(file_path)
        == "This is a paragraph. This is another paragraph. § 1. This is yet another paragraph. Załącznik nr 1 This is an attachment."
    )


def test_jsonize_pdf_1():
    text = (
        "1. Nazwa przedmiotu praktyka 2. Forma zajęć praktyka 3. Rok akademicki, rok studiów, semestr realizacji przedmiotu rok III semestr II 4. Stopień studiów, tryb studiów brak 5. Cel przedmiotu brak 6. Wymagania wstępne brak 7. Metody kształcenia praktyka 8.",
    )

    assert parser.jsonize_pdf(text[0]) == {
        "Nazwa przedmiotu": "praktyka",
        "Forma zajęć": "praktyka",
        "Rok akademicki, rok studiów, semestr realizacji przedmiotu": "rok III semestr II",
        "Stopień studiów, tryb studiów": "brak",
        "Cel przedmiotu": "brak",
        "Wymagania wstępne": "brak",
        "Metody kształcenia": "praktyka",
    }


def test_jsonize_pdf_2():
    text = "1. Nazwa przedmiotu praktyka 2."
    assert parser.jsonize_pdf(text) == {"Nazwa przedmiotu": "praktyka"}


def test_get_raw_text_from_tables():
    file_path = r"tests/test_files/test_table_file.pdf"
    iterator = 1
    pdf_doc = pdf.Document(file_path)
    assert (
        parser.get_raw_text_from_tables(pdf_doc, iterator)
        == "Text1 Text2 Obj2 Obj33 Obj1 Obj22"
    )
