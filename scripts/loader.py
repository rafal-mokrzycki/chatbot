from uuid import uuid4

import pinecone
import tiktoken
from config import load_config
from datasets import load_dataset
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm.auto import tqdm

config = load_config()


class PineconeIndex:
    def __init__(self) -> None:
        pinecone.init(
            api_key=config["PINECONE_API_KEY"], environment=config["PINECONE_ENV"]
        )
        self.index_name = config["INDEX_NAME"]
        if self.index_name not in pinecone.list_indexes():
            self.create_index()
        self.index = pinecone.Index(self.index_name)

    def create_index(self) -> None:
        """
        Creates index if not exists.
        """
        if self.index_name not in pinecone.list_indexes():
            # we create a new index
            pinecone.create_index(
                name=self.index_name,
                metric="cosine",
                dimension=1536,
            )
        else:
            print(f"Index {self.index_name} already exists.")
        # return pinecone.Index(self.index_name)

    def _delete_index(self) -> None:
        """
        Deletes index.
        """
        pinecone.delete_index(self.index_name)

    def load_data_into_index(self, data_files: str):
        """
        Loads data to index.

        Args:
            data_files (str): data file to preprocess and load into the index.
        """
        # settings
        data = load_dataset("csv", split="train", data_files=data_files, sep=";")
        if data_files == "sentences_raw.csv":
            namespace = config["PINECONE_NAMESPACE_RAW"]
        else:
            namespace = config["PINECONE_NAMESPACE_TAGGED"]
        texts = []
        metadatas = []

        for _, record in enumerate(tqdm(data)):
            # first get metadata fields for this record
            if data_files == "sentences_raw.csv":
                metadata = {"answers": record["answers"], "source": ""}
            else:
                metadata = {
                    "id": str(record["id"]),
                    "title": record["title"],
                    "context": record["context"],
                    "question": record["question"],
                    "answers": record["answers"],
                    "source": "",
                }
            # now we create chunks from the record text
            record_texts = TextProcessing().text_splitter.split_text(record["answers"])
            # create individual metadata dicts for each chunk
            record_metadatas = [
                {"chunk": j, "answers": text, **metadata}
                for j, text in enumerate(record_texts)
            ]
            # append these to current batches
            texts.extend(record_texts)
            metadatas.extend(record_metadatas)
            # if we have reached the batch_limit we can add texts
            if len(texts) >= config["BATCH_LIMIT"]:
                ids = [str(uuid4()) for _ in range(len(texts))]
                embeds = TextProcessing().embed.embed_documents(texts)
                self.index.upsert(
                    vectors=zip(ids, embeds, metadatas), namespace=namespace
                )
                texts = []
                metadatas = []

        if len(texts) > 0:
            ids = [str(uuid4()) for _ in range(len(texts))]
            embeds = TextProcessing().embed.embed_documents(texts)
            self.index.upsert(vectors=zip(ids, embeds, metadatas), namespace=namespace)

    def _delete_data(self, namespace: str) -> None:
        """
        Deletes data in a given namespace.

        Args:
            namespace (str): Namespace to delete data in.
        """
        self.index.delete(delete_all=True, namespace=namespace)

    def __repr__(self):
        return pinecone.describe_index(self.index_name)

    def __info__(self):
        return self.index.describe_index_stats()


class TextProcessing:
    def __init__(self) -> None:
        self.tokenizer = tiktoken.get_encoding(config["TIKTOKEN_ENCODING"])
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=20,
            length_function=self.tiktoken_len,
            separators=["\n\n", "\n", " ", ""],
        )
        self.embed = OpenAIEmbeddings(
            model=config["OPEN_AI_MODEL_NAME"], openai_api_key=config["OPENAI_API_KEY"]
        )

    def get_split_text(self, data):
        return self.text_splitter.split_text(data[6]["answers"])[:3]

    def tiktoken_len(self, text):
        tokens = self.tokenizer.encode(text, disallowed_special=())
        return len(tokens)
