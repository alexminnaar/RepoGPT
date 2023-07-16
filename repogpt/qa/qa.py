from langchain.vectorstores import DeepLake
from langchain.llms import BaseLLM
from langchain.docstore.document import Document
from typing import List


class QA:

    def __init__(self, llm: BaseLLM, deeplake_store: DeepLake):
        self.llm = llm
        self.retriever = deeplake_store.as_retriever()
        self.retriever.search_kwargs['distance_metric'] = 'cos'
        self.retriever.search_kwargs['fetch_k'] = 20
        self.retriever.search_kwargs['maximal_marginal_relevance'] = False
        self.retriever.search_kwargs['k'] = 15

    def create_prompt(self, query_str: str, similar_chunks: List[Document]) -> str:
        """Build the final prompt string using query and similar chunks"""
        similar_chunk_str = '\n'.join([chunk.page_content for chunk in similar_chunks])
        # TODO: add to prompt to not use test files if query does not explicitly mention test files
        # TODO: Try structured json prompt
        final_prompt = f"Given these code snippets, \n {similar_chunk_str}\n The question is: {query_str}"
        return final_prompt

    def get_resp(self, query_str: str) -> str:
        """Given a string, get similar chunks and construct a prompt feed it to LLM and return response"""
        # reverse similar chunks so that most relevant are less likely to be forgotten
        similar_chunks = self.retriever.get_relevant_documents(query_str)[::-1]
        for chunk in similar_chunks:
            print(chunk.metadata['source'])
        qa_prompt = self.create_prompt(query_str, similar_chunks)
        return self.llm(qa_prompt)