import os

import repackage

repackage.up()
from config.config import load_config

config = load_config()


class Preprocessor:
    """
    Class for preprocessing of DOCX and PDF files. Takes a file or a directory with files.
    """

    def __init__(self, path: str | None = None) -> None:
        self.path = path
        self.files_list = self.search_files_in_dir()

    def search_files_in_dir(self, path_to_search: str | None = None):
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
