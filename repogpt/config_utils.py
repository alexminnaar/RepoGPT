from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import OpenAI
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

    if config.has_section("embeddings"):

        embedding_name = get_config_option(config, "hf-embeddings", "EMBEDDING_TYPE")

        if embedding_name == "openai":
            embeddings = OpenAIEmbeddings()
        elif embedding_name == "huggingface":
            embeddings = HuggingFaceEmbeddings()
        else:
            raise ValueError("RepoGPT currently only supports 'openai' or 'huggingface' embeddings!")
    else:
        raise ValueError("Config file must contain 'embeddings' section!")

    return embeddings


def read_config_dir_paths(config_file: str) -> [str, str]:
    """Get repo and vector store paths from config file"""
    config = configparser.ConfigParser()
    config.read(config_file)

    _repo_path = get_config_option(config, "repo", "REPO_PATH")
    _vs_path = get_config_option(config, "vectorstore", "VS_PATH")

    return _repo_path, _vs_path


def read_config_llm(config_file: str) -> BaseLLM:
    """Initialize LLM object based on type specified in config file"""
    config = configparser.ConfigParser()
    config.read(config_file)

    if config.has_section("openai-llm"):
        llm_name = get_config_option(config, "openai-llm", "OPENAI_MODEL_NAME")
        llm = OpenAI(model_name=llm_name)
    elif config.has_section("local-llm"):
        llm_name = get_config_option(config, "local-llm", "LOCAL_LLM_NAME")
        llm_path = get_config_option(config, "local-llm", "LOCAL_LLM_PATH")
        # TODO: Change this to local llm
        llm = OpenAI(model_name='gpt-3.5-turbo-16k')

    else:
        raise ValueError("Config file must contain either openai-llm or local-llm sections!")

    return llm
