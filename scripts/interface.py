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

    def talk(self, text_field="answers", prettify=True):
        vectorstore = Pinecone(
            pinecone_index.index, text_processing.embed.embed_query, text_field
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
        i = 1
        for query in queries:
            print(i)
            if prettify:
                print(qa.run(query))
            else:
                res = vectorstore.similarity_search(
                    query, k=2  # our search query  return 2 most relevant docs
                )
                print(res[0])

            # qa_with_sources = RetrievalQAWithSourcesChain.from_chain_type(
            #     llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever()
            # )
            # print(qa_with_sources(query))
            # else:
            #     print("NOT IN KB")
            i += 1
