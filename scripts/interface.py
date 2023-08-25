from config import load_config
from langchain.vectorstores import Pinecone
from loader import PineconeIndex, TextProcessing

config = load_config()
pinecone_index = PineconeIndex()
text_processing = TextProcessing()


class UserInterface:
    def __init__(self) -> None:
        super().__init__()

    def make_conversation(
        self,
        query: str,
        namespace: str = None,
        threshold: float = None,
        text_field: str = None,
    ) -> str:
        """
        Takes user query as input and returns an answer based on KB (if available)
        or says it doesn't know.

        Args:
            query (str): user query.
            namespace (str, optional): Namespace in Pinecone index to search information
            in. Defaults to None. TODO: probably will be deprecated as determining
            a namespace based on user input using LM is planned.
            threshold (float, optional): Threshold below which no valid information is
            returned (as the answer for the query is not in KB). Defaults to None.
            text_field (str, optional): Field in Pinecone index to search answer for.
            Defaults to None.

        Returns:
            str: Answer for user question.
        """
        if namespace is None:
            namespace = config["pinecone"]["namespace"]["raw"]
        if threshold is None:
            threshold = config["openai"]["threshold"]
        if text_field is None:
            text_field = "answers"
        vectorstore = Pinecone(
            index=pinecone_index.index,
            embedding=text_processing.embed.embed_query,
            text_key=text_field,
            namespace=namespace,
        )
        res = vectorstore.similarity_search_with_score(query, k=1, namespace=namespace)
        # res is a list of tuples, where 1st elem is a Document object with 2 attrs:
        # page_content (str) and metadata (dict) and 2nd is a score (distance from
        # question to the nearest answer)
        if res[0][1] > threshold:
            return res[0][0].page_content
        return str("Not in KB.")
