"""!pip install farm-haystack[sql]"""

import os
import json

from haystack import Document
from haystack.nodes import EmbeddingRetriever
from haystack.document_stores import InMemoryDocumentStore, SQLDocumentStore
from haystack.schema import Document

def create_document_store(squrl: str="sqlite:///wikitext.sqlite.db"):
    if squrl is None:
        # Write documents to InMemoryDocumentStore
        return InMemoryDocumentStore()

    return SQLDocumentStore(url=squrl, index="document")


def ingest_json_to_document_store(json_fname: str):

    # Load JSON data
    with open(json_fname, "r") as file:
        data = json.load(file)
        documents = [
            Document(content=doc["content"], meta=doc.get("meta"))
            for doc in data
        ]

    # Write documents to the DocumentStore
    document_store.write_documents(documents)

    # Add embeddings to the documents in the DocumentStore
    document_store.update_embeddings(retriever)
    return document_store



documents = []

# json_fname = "./excellent-articles/excellent-articles.json"
json_fname = "dummy.json"

if os.path.isfile(json_fname):
    document_store = ingest_json_to_document_store(
        json_fname=json_fname
    )
else:
    documents = [
        Document(
            content="My name is Asra, I live in Paris.",
            meta={"src": "doc_1"}
        ),
        Document(
            content="My name is Lee, I live in Berlin.",
            meta={"src": "doc2"}
        ),
        Document(
            content="My name is Giorgio, I live in Rome.",
            meta={"src": "doc_3"}
        ),
    ]


document_store.write_documents(documents)
