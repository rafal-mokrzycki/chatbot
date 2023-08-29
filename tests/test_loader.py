# to run: .venv/Scripts/python.exe -m pytest -vv  tests/test_loader.py -s
from pathlib import Path, WindowsPath

import pinecone
import pytest
import repackage
from datasets import load_dataset

repackage.up()
from scripts.interface import PineconeIndex, TextProcessing
from scripts.loader import convert_path_to_string


# TODO: more fixtures
@pytest.fixture(name="pinecone_index_name")
def pinecone_index_name():
    yield "lazarski-test"


@pytest.fixture(name="filepath")
def sample_file_path():
    yield str(Path(__file__).parent.joinpath("sample.csv"))


@pytest.fixture(name="not_existing_file_path")
def not_existing_file_path():
    yield r"tests\test_files\not_existing_file.pdf"


@pytest.fixture(name="existing_file_path")
def existing_file_path():
    yield r"tests\test_files\test_file.pdf"


def test_create_index(pinecone_index_name):
    pi = PineconeIndex(index_name=pinecone_index_name)
    pi.create_index()
    assert pinecone_index_name in pinecone.list_indexes()
    pinecone.delete_index(pinecone_index_name)


def test_delete_index(pinecone_index_name):
    pi = PineconeIndex(index_name=pinecone_index_name)
    pi.create_index()
    pi._delete_index()
    assert pinecone_index_name not in pinecone.list_indexes()


def test_load_data_into_index(filepath, pinecone_index_name):
    pi = PineconeIndex(index_name=pinecone_index_name)
    pi.create_index()
    pi.load_data_into_index(filepath)
    description = pi.index.describe_index_stats()
    assert description["total_vector_count"] == 1
    pinecone.delete_index(pinecone_index_name)


def test_delete_data(filepath, pinecone_index_name):
    pi = PineconeIndex(index_name=pinecone_index_name)
    pi.create_index()
    pi.load_data_into_index(filepath)
    pi._delete_data(namespace="sentences_raw")
    description = pi.index.describe_index_stats()
    assert description["total_vector_count"] == 0
    pinecone.delete_index(pinecone_index_name)


def test_get_split_text(filepath):
    tp = TextProcessing()
    dataset = load_dataset("csv", split="train", data_files=filepath, sep=";")
    text = tp.get_split_text(dataset)
    assert len(text) == 1


def test_tiktoken_len():
    tp = TextProcessing()
    text = "I am now evaluating a mechanism that uses index for an embedding space."
    assert tp.tiktoken_len(text) == 14


def test_convert_path_to_string_1(existing_file_path):
    assert convert_path_to_string(existing_file_path) == existing_file_path


def test_convert_path_to_string_2(existing_file_path):
    path = Path(existing_file_path)
    assert convert_path_to_string(path) == existing_file_path


def test_convert_path_to_string_3(existing_file_path):
    path = WindowsPath(existing_file_path)
    assert convert_path_to_string(path) == existing_file_path


def test_convert_path_to_string_4(not_existing_file_path):
    with pytest.raises(TypeError, match="Path must be a valid file path."):
        convert_path_to_string(not_existing_file_path)


def test_convert_path_to_string_5(not_existing_file_path):
    path = Path(not_existing_file_path)
    with pytest.raises(TypeError, match="Path must be a valid file path."):
        convert_path_to_string(path)


def test_convert_path_to_string_6(not_existing_file_path):
    path = WindowsPath(not_existing_file_path)
    with pytest.raises(TypeError, match="Path must be a valid file path."):
        convert_path_to_string(path)


def test_convert_path_to_string_7():
    with pytest.raises(TypeError, match="Path must be a string, Path or WindowsPath."):
        convert_path_to_string(0)


def test_convert_path_to_string_8():
    with pytest.raises(TypeError, match="Path must be a string, Path or WindowsPath."):
        convert_path_to_string(0.0)


def test_convert_path_to_string_9():
    with pytest.raises(TypeError, match="Path must be a string, Path or WindowsPath."):
        convert_path_to_string(True)
