# RepoGPT
An LLM-based coding mentor for your repository

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

A chunk like this can be retrieved from the vector store and passed into a prompt for the LLM, however it was found that
the LLM responses would often be wrong due to a lack of context around this chunk.  To fix this, RepoGPT adds additional 
context to the chunk including the file name and file path associated with the chunk as well as a summary of the file the 
chunk was taken from and the line number where the chunk appears in the file.  This additional contextual information
seems to improve the LLM's responses.
 
## Usage

### Create a config.ini File
The `config.ini` file sets the parameters that RepoGPT needs to run.  They are

* `REPO_PATH`: The path to the root directory of the git repo.
* `VS_PATH`: The path where the vector store will be created.
* `EMBEDDING_TYPE`: The name of the embedding being used - currently this can only take value 'openai' or 'huggingface'.
* `OPENAI_MODEL_NAME`: The name of the OpenAI model to use e.g. `gpt-3.5-turbo-16k`.

An example `config.ini` would look like

```
[repo]
REPO_PATH = /my/repo/path

[vectorstore]
VS_PATH = /my/vs/path

[embeddings]
EMBEDDING_TYPE = openai

[openai-llm]
OPENAI_MODEL_NAME = gpt-3.5-turbo-16k
```

### Initialize Repo
This step crawls and indexes the repo specified in `example_config.ini`.
```commandline
python repogpt/cli/cli.py --init example_config.ini
```

### Ask Questions
Run the command
```commandline
python repogpt/cli/cli.py example_config.ini 
```
you should then see

```commandline
Ask a question: 
```
Then ask your question and wait for the response.

## Testing

```commandline
python -m pytest
```
