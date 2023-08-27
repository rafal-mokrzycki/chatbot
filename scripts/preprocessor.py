import os
import re
from pathlib import Path

import aspose.pdf as pdf
import repackage
from docx import Document

repackage.up()
from config.config import load_config

config = load_config()


class Preprocessor:
    """
    Class for preprocessing of DOCX and PDF files. Takes a file or a directory with files.
    """

    def __init__(self, path: str | None = None) -> None:
        if path is None:
            path = Path(__file__).parent.parent.joinpath("data")
        self.path = path
        self.files_list = self.search_files_in_dir()

    def search_files_in_dir(self, path_to_search: str | None = None) -> list:
        """
        Searches all files in a dir (checking also subdirs) that have extensions as
        in config.json.

        Args:
            path_to_search (str | None, optional): Path to search files in. If None,
            equals to self.path. Defaults to None.

        Returns:
            list: List of files with absolute paths.
        """
        if path_to_search is None:
            path_to_search = self.path
        if os.path.isfile(path_to_search):
            return [path_to_search]
        elif os.path.isdir(path_to_search):
            file_paths = []
            for root, _, files in os.walk(path_to_search):
                for file in files:
                    _, ext = os.path.splitext(file)
                    if ext.lower() in config["general"]["accepted_file_formats"]:
                        file_path = os.path.join(root, file)
                        file_paths.append(os.path.abspath(file_path))
            return file_paths

    def extract_sentences_from_docx(self, file_path):
        doc = Document(file_path)
        text = " ".join([paragraph.text for paragraph in doc.paragraphs])
        return text

    def get_raw_text_from_pdf(self, file_path: str) -> str:
        """
        Returns raw text (single string) from a PDF file.

        Args:
            file_path (str): File path to read PDF file from.

        Returns:
            str: Full text of a PDF file
        """
        pdfDocument = pdf.Document(file_path)
        full_text = []
        for i in range(0, len(pdfDocument.pages) - 1):
            full_text.append(self.get_raw_text_from_tables(pdfDocument, i + 1))
        return "".join(full_text).replace("  ", " ")

    def get_raw_text_from_tables(self, pdfDocument: pdf.Document, iterator: int) -> str:
        """
        Returns raw text (single string) from a table in a PDF file.

        Args:
            pdfDocument (pdf.Document): PDF pages.
            iterator (int): Number of page.

        Returns:
            str: Full text of a PDF file page.
        """
        # Initialize TableAbsorber object
        tableAbsorber = pdf.text.TableAbsorber()

        # Parse all the tables on first page
        tableAbsorber.visit(pdfDocument.pages[iterator])

        # Get a reference of the first table
        absorbedTable = tableAbsorber.table_list[0]

        full_text = []

        # Iterate through all the rows in the table
        for pdfTableRow in absorbedTable.row_list:
            # Iterate through all the columns in the row
            for pdfTableCell in pdfTableRow.cell_list:
                # Fetch the text fragments
                textFragmentCollection = pdfTableCell.text_fragments
                # Iterate through the text fragments
                for textFragment in textFragmentCollection:
                    # Print the text
                    full_text.extend(textFragment.text)
        return "".join(full_text).replace("  ", " ")

    def jsonize_pdf(self, main_string: str) -> dict:
        """
        Gets saught after elements and return them as a dict, eg.
        dict['Metody kształcenia'] = 'Wskazane przez praktykodawcę'

        Args:
            main_string (str): String to search in.

        Returns:
            dict: Dictionary with `headers` as keys and information as values.
        """
        json_ = {}
        list_of_headers = [
            "Nazwa przedmiotu",
            "Forma zajęć",
            "Rok akademicki, rok studiów, semestr realizacji przedmiotu",
            "Stopień studiów, tryb studiów",
            "Cel przedmiotu",
            "Wymagania wstępne",
            "Metody kształcenia",
        ]
        for elem in list_of_headers:
            json_[elem] = self.forward_regexp_search(main_string, elem)
        return json_

    def forward_regexp_search(self, main_string: str, target_string: str) -> str:
        """
        Searches a given substring (`target_string`) in a large string (`main_string`)
        and returns N next words as one string (up to the nearest number with a comma, eg.
        `13.`)

        Args:
            main_string (str): String to search in
            target_string (str): Subtring to search

        Returns:
            str: Searched string.
        """

        def get_number_with_comma(string):
            regexp = r"\d+\."
            if re.fullmatch(regexp, string) is not None:
                return False
            return True

        # get rid of whitespaces at the beginning and in the end
        target_string = target_string.strip()
        length = len(target_string)
        # position of the target_string
        pos = main_string.find(target_string)
        word_list = (main_string[pos + length :].strip()).split(" ")
        result = []
        for word in word_list:
            if get_number_with_comma(word):
                result.append(word)
            else:
                break
        return " ".join(result)
