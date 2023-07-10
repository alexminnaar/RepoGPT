from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake


class QA:

    def __init__(self, db_location: str):
        self.model = ChatOpenAI(model_name='gpt-3.5-turbo-16k')
        self.embedding_model = OpenAIEmbeddings()
        self.db = DeepLake(dataset_path=db_location, read_only=True, embedding_function=self.embedding_model)
        self.retriever = self.db.as_retriever()
        self.retriever.search_kwargs['distance_metric'] = 'cos'
        self.retriever.search_kwargs['fetch_k'] = 20
        self.retriever.search_kwargs['maximal_marginal_relevance'] = False
        self.retriever.search_kwargs['k'] = 3
        self.qa_chain = ConversationalRetrievalChain.from_llm(self.model, retriever=self.retriever,
                                                              return_source_documents=True)

    def query(self, query_str: str) -> str:
        return self.qa_chain({"question": query_str, "chat_history":[]})['answer']