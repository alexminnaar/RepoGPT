from langchain.vectorstores import DeepLake
from langchain.llms import BaseLLM
from langchain.docstore.document import Document
from typing import List
from colorama import Fore, Back, Style, init

init(autoreset=True)


class QA:

    def __init__(self, llm: BaseLLM, deeplake_store: DeepLake, num_results: int):
        self.llm = llm
        self.retriever = deeplake_store.as_retriever()
        self.retriever.search_kwargs['distance_metric'] = 'cos'
        self.retriever.search_kwargs["fetch_k"] = 100
        self.retriever.search_kwargs['maximal_marginal_relevance'] = False
        self.retriever.search_kwargs['k'] = num_results

    def create_prompt(self, query_str: str, similar_chunks: List[Document]) -> str:
        """Build the final prompt string using query and similar chunks"""
        similar_chunk_str = '\n'.join([chunk.page_content for chunk in similar_chunks])
        # TODO: Try structured json prompt
        final_prompt = f"You will be asked a question based on the following code snippets, \n {similar_chunk_str}\n " \
                       f"You may need to combine the above snippets according to their line numbers to answer the " \
                       f"following question.  The question is: {query_str}"
        return final_prompt

    def get_resp(self, query_str: str) -> str:
        """Given a string, get similar chunks and construct a prompt feed it to LLM and return response"""
        # reverse similar chunks so that most relevant are less likely to be forgotten
        similar_chunks = self.retriever.get_relevant_documents(query_str)[::-1]
        print(Fore.RED + "Relevant files:")
        for chunk in similar_chunks:
            print(Fore.RED +
                  f"{chunk.metadata['source']} - lines {chunk.metadata['starting_line']} - {chunk.metadata['ending_line']}")

        qa_prompt = self.create_prompt(query_str, similar_chunks)
        print("Computing response...")
        return self.llm(qa_prompt)
