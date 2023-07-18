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

This additional contextual information seems to improve the LLM's responses.
 
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

## Usage

### 1. Create a config.ini File
The `config.ini` file sets the parameters that RepoGPT needs to run.  They are

* `REPO_PATH`: The path to the root directory of the git repo.
* `VS_PATH`: The path where the vector store will be created.
* `NUM_RESULTS`: The number of search results returned by the vector store for a given query.
* `EMBEDDING_TYPE`: The name of the embedding being used.
* `MODEL_NAME`: The name of the LLM to use.

Example `config.ini` files can be found in the `example_config_files` directory in this repo.


### 2. Initialize Repo
This step crawls and indexes the repo specified in `example_config.ini`.
```commandline
python repogpt/cli/cli.py --init example_config.ini
```

### 3. Ask Questions
Run the command
```commandline
python repogpt/cli/cli.py example_config.ini 
```
you should then see

```commandline
Ask a question: 
```
Then ask your question and wait for the response.


