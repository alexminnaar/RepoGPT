from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import OpenAI, GPT4All, LlamaCpp
from langchain.embeddings.base import Embeddings
from langchain.llms import BaseLLM
from typing import Optional
import configparser


def get_config_option(config, section: str, option: str) -> Optional[str]:
    """Get option from section of config file if it exists"""
    if config.has_section(section) and config.has_option(section, option):
        return config.get(section, option)
    else:
        raise ValueError(f"config file does not contain {section} section and {option} option!")


def read_config_embeddings(config_file: str) -> Embeddings:
    """Initialize the embeddings object based on type specified in config file"""
    config = configparser.ConfigParser()
    config.read(config_file)

    if config.has_section("openai-embeddings"):
        embedding_name = get_config_option(config, "openai-embeddings", "EMBEDDING_TYPE")
        embeddings = OpenAIEmbeddings()
    elif config.has_section("hf-embeddings"):
        embedding_name = get_config_option(config, "hf-embeddings", "EMBEDDING_TYPE")
        embeddings = HuggingFaceEmbeddings(model_name=embedding_name)
    else:
        raise ValueError("Config file must contain 'embeddings' section!")

    return embeddings


def read_config_dir_paths(config_file: str) -> [str, str]:
    """Get repo and vector store paths from config file"""
    config = configparser.ConfigParser()
    config.read(config_file)

    _repo_path = get_config_option(config, "repo", "REPO_PATH")
    _vs_path = get_config_option(config, "vectorstore", "VS_PATH")
    _vs_num_results = get_config_option(config, "vectorstore", "NUM_RESULTS")
    _chunk_size = get_config_option(config, "crawler", "CHUNK_SIZE")
    _chunk_overlap = get_config_option(config, "crawler", "CHUNK_OVERLAP")

    return _repo_path, _vs_path, int(_vs_num_results), int(_chunk_size), int(_chunk_overlap)


def read_config_llm(config_file: str) -> BaseLLM:
    """Initialize LLM object based on type specified in config file"""
    config = configparser.ConfigParser()
    config.read(config_file)

    if config.has_section("openai-llm"):
        llm_name = get_config_option(config, "openai-llm", "MODEL_NAME")
        llm = OpenAI(model_name=llm_name)
    elif config.has_section("local-llm"):
        llm_path = get_config_option(config, "local-llm", "MODEL_PATH")
        llm_name = get_config_option(config, "local-llm", "MODEL_NAME")
        model_n_ctx = get_config_option(config, "local-llm", "MODEL_N_CTX")
        model_n_batch = get_config_option(config, "local-llm", "MODEL_N_BATCH")
        if llm_name == "GPT4All":
            llm = GPT4All(model=llm_path, n_ctx=model_n_ctx, backend='gptj', n_batch=model_n_batch)
        elif llm_name == "LlamaCpp":
            llm = LlamaCpp(model_path=llm_path, n_ctx=model_n_ctx, n_batch=model_n_batch)
        else:
            raise ValueError("RepoGPT only supports GPT4All and LlamaCpp local models!")
    else:
        raise ValueError("Config file must contain either openai-llm or local-llm sections!")

    return llm
