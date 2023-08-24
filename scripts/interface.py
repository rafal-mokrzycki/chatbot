from config import load_config
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
from loader import PineconeIndex, TextProcessing

config = load_config()
pinecone_index = PineconeIndex()
text_processing = TextProcessing()


class Interface:
    def __init__(self) -> None:
        super().__init__()

    def prettify(self, text: str) -> str:
        """
        Helper func for prettifying an answer. Not implemented yet.

        Args:
            text (str): Text to apply prettifying model on.

        Returns:
            str: Prettified text.
        """
        # TODO: implement

        return text

    def talk(self, text_field: str = "answers"):
        """Not fully implemented yet."""
        # TODO: implement
        vectorstore = Pinecone(
            index=pinecone_index.index,
            embedding=text_processing.embed.embed_query,
            text_key=text_field,
            namespace=config["pinecone"]["namespace"]["raw"],
        )

        queries = [
            "Jakie powinny być marginesy w pracy?",
            "Jak zmienić promotora?",
            "Czy mogę zmienić formę studiów?",
            "Kim był Kopernik?",
            "Kiedy wybuchła I wojna światowa?",
            "Ile mieszkańców ma Warszawa?",
        ]
        # completion llm
        llm = ChatOpenAI(
            openai_api_key=config["openai"]["api_key"],
            model_name=config["pinecone"]["model_name"],
            temperature=0.0,
        )
        qa = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever()
        )
        for query in queries:
            res = vectorstore.similarity_search_with_score(
                query, k=3, namespace=config["pinecone"]["namespace"]["raw"]
            )
            # res is a list of tuples, where 1st elem is a Document object with 2 attrs:
            # page_content (str) and metadata (dict) and 2nd is a score (distance from
            # question to the nearest answer)
            if res[0][1] > 0.8:
                print(self.prettify(res[0][0].page_content))
            else:
                print("Not in KB.")
