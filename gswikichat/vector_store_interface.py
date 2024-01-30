import os
import json

from haystack import Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever

top_k = 5
documents = []

if os.path.isfile("./json_input/excellent-articles.json"):
    with open("./json_input/excellent-articles.json", 'r') as f:
        json_obj = json.load(f)
        for k, v in json_obj.items():
            print(f"Loading {k}")
            documents.append(Document(content=v, meta={"src": k}))
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

# Write documents to InMemoryDocumentStore
document_store = InMemoryDocumentStore()
document_store.write_documents(documents)

retriever = InMemoryBM25Retriever(
    document_store=document_store,
    top_k=top_k
)
