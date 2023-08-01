from langchain.vectorstores import DeepLake
from repogpt.crawler import crawl_and_split, index
from repogpt.qa.qa import QA
from repogpt import config_utils
import argparse
import logging
from colorama import Fore, Back, Style, init

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("repogpt_cli_logger")

init(autoreset=True)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", "-I", action='store_true', help='Use this flag to crawl and index repository')
    parser.add_argument('config_file', help='Path to the config file')
    return parser.parse_args()


def main():
    args = parse_arguments()

    # create embedding object - required for both indexing and qa
    embeddings = config_utils.read_config_embeddings(args.config_file)

    # get paths to repository to crawl, vector store and num results to extract from vector store per query
    repo_path, vs_path, num_results, chunk_size, chunk_overlap = config_utils.read_config_dir_paths(args.config_file)

    # if running in init mode, just crawl and index the repo
    if args.init:
        logger.info("Crawling repo...")
        repo_docs = crawl_and_split(repo_path, chunk_size, chunk_overlap)
        index(repo_docs, embeddings, vs_path)
        logging.info(f"chunks successfully indexed to vector store located at {repo_path}")

    # running in qa mode
    else:
        logger.info("Initializing LLM...")
        llm = config_utils.read_config_llm(args.config_file)
        vs = DeepLake(dataset_path=vs_path, read_only=True, embedding_function=embeddings)
        qa = QA(llm, vs, num_results)

        while True:
            query = input("\nAsk a question: ")
            if query == "exit":
                break
            if query.strip() == "":
                continue

            try:
                resp = qa.get_resp(query)
                print(Fore.GREEN + f"Response:\n{resp}")
            except Exception as e:
                logger.error(f"Exception occurred computing LLM Response: {e}")


if __name__ == "__main__":
    main()
