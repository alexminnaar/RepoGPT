# RepoGPT
An LLM-based coding mentor for your repository

## Install

## What is RepoGPT?

Say you are introduced to a new code repository that you know nothing about.  RepoGPT is a tool that allows you to gain 
a better understanding of your repository by asking an LLM questions about it.

## How does it work?

When RepoGPT is initialized for a given repository it crawls the files in the repository and for each file it parses the 
code structure, splits the file into chunks, generates vector embeddings for each chunk and indexes them into a vector 
database.  Once this is done you can start asking questions.  The way question answering works is you submit a query, 
the query is translated into an embedding vector, the vector database is queried against this vector and similar file
chunks are returned.  The query and similar chunks are then made into a prompt for an LLM and the response is returned
which contains an answer to your question.

## Usage


## Testing

```commandline
python -m pytest
```
