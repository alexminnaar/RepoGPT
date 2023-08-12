# 🔎 RepoGPT
An LLM-based coding mentor for your repository

![build](https://github.com/alexminnaar/repogpt/actions/workflows/ci.yml/badge.svg)

## What is RepoGPT?

Say you are introduced to a new code repository that you know nothing about.  RepoGPT is a tool that allows you to gain 
a better understanding of your repository by giving you the ability to ask an LLM questions about it.

## How does it Work?

When RepoGPT is initialized for a given repository it crawls the files in the repository and for each file it parses the 
code structure, splits the file into chunks, generates vector embeddings for each chunk and indexes them into a vector 
database.  Once this is done you can start asking questions which is done by translating the query into an embedding 
vector which is then used to query a vector database and similar file chunks are returned.  The query and similar chunks
are then made into a prompt for an LLM and the response is returned which contains an answer to your question.

### Chunking with Context

It was found that the LLM responses would often be wrong due to a lack of context around the chunk.  To fix this, 
RepoGPT adds additional context to the chunk including
* The file name and file path associated with the chunk.
* A summary of the classes and methods contained in the file.
* The line number where the chunk appears in the file.  

For example, a RepoGPT chunk may look like

```
The following code snippet is from a file at location /langchain/langchain/embeddings/aleph_alpha.py 
starting at line 74 and ending at line 98.   The last class defined before this snippet was called 
`AlephAlphaAsymmetricSemanticEmbedding` starting at line 9 and ending at line 142.  The last method starting before this 
snippet is called `embed_documents` which starts on line 68 and ends at line 107. The code snippet starting at line 
74 and ending at line 98 is 
'''
        Returns:
            List of embeddings, one for each text.
        """
        try:
            from aleph_alpha_client import (
                Prompt,
                SemanticEmbeddingRequest,
                SemanticRepresentation,
            )
        except ImportError:
            raise ValueError(
                "Could not import aleph_alpha_client python package. "
                "Please install it with `pip install aleph_alpha_client`."
            )
        document_embeddings = []

        for text in texts:
            document_params = {
                "prompt": Prompt.from_text(text),
                "representation": SemanticRepresentation.Document,
                "compress_to_size": self.compress_to_size,
                "normalize": self.normalize,
                "contextual_control_threshold": self.contextual_control_threshold,
                "control_log_additive": self.control_log_additive,
            }
'''           
```

## Usage

### 1. Create a config.ini File
The `config.ini` file sets the parameters that RepoGPT needs to run.  They are

* `REPO_PATH`: The path to the root directory of the git repo.
* `VS_PATH`: The path where the vector store will be created.
* `NUM_RESULTS`: The number of search results returned by the vector store for a given query.
* `EMBEDDING_TYPE`: The name of the embedding being used.
* `MODEL_NAME`: The name of the LLM to use.
* `CHUNK_SIZE`: The size (in tokens) of the chunks the files are split into.
* `CHUNK_OVERLAP`: The size (in tokens) of the overlap in subsequent chunks.

Example `config.ini` files can be found in the `example_config_files` directory in this repo.


### 2. Initialize Repo
This step crawls and indexes the repo specified in `example_config.ini`.
```commandline
python cli.py --init example_config.ini
```

### 3. Ask Questions
Run the command
```commandline
python cli.py example_config.ini 
```
you should then see

```commandline
Ask a question: 
```
Then ask your question and wait for the response.  To exit, type 'exit'.

## Demo

In this demo, the [Pandas](https://github.com/pandas-dev/pandas/tree/main) python library repo has been crawled and 
we will ask RepoGPT some questions about it.  This demo's config.ini file specifies `sentence-transformers/all-mpnet-base-v2` 
huggingface embeddings and OpenAI's `gpt-4` model.
### Use Case #1: Code Search

With RepoGPT you can search for a piece of code.  For example, let's ask RepoGPT to "show the `value_counts` method in
the `ArrowExtensionArray` class".

![demo1](https://github.com/alexminnaar/RepoGPT/blob/main/assets/repogpt_demo1.png "demo1")

### Use Case #2: Code Understanding

RepoGPT can also explain pieces of code.  For example, let's ask RepoGPT to "explain the `value_counts` method in
the `ArrowExtensionArray` class".

![demo2](https://github.com/alexminnaar/RepoGPT/blob/main/assets/repogpt_demo2.png "demo2")


### Use Case #3: Code Writing

RepoGPT can also write new code based on the repo.  For example let's ask RepoGPT to "write unit tests for the 
`value_counts` method in the `ArrowExtensionArray` class".

![demo3](https://github.com/alexminnaar/RepoGPT/blob/main/assets/repogpt_demo3.png "demo3")

 
## Supported Languages

The following languages/file types can be crawled with RepoGPT

* Python
* C++
* JAVA
* GO
* Javascript/Typescript
* PHP
* Protobuf
* Rust
* Ruby
* Scala
* Swift
* Markdown
* Latex
* HTML

## Supported LLMs

* OpenAI
* LLama.cpp (experimental)
* GPT4ALL (experimental)

## Supported Embeddings

* OpenAI
* HuggingFace

⚠️ Warning: Crawling a large repo while using OpenAI embeddings could result in many thousands of embedding requests ⚠️




