# to run: .venv/Scripts/python.exe -m pytest -vv  tests/test_loader.py -s
from pathlib import Path

import pinecone
import pytest
import repackage
from datasets import load_dataset

repackage.up()
from scripts.interface import PineconeIndex, TextProcessing


# TODO: more fixtures
@pytest.fixture(name="pinecone_index_name")
def pinecone_index_name():
    yield "lazarski-test"


@pytest.fixture(name="filepath")
def sample_file_path():
    yield str(Path(__file__).parent.joinpath("sample.csv"))


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
    text = "I am now evaluating a mechanism that using index for an embedding space."
    assert tp.tiktoken_len(text) == 14
