
"""
# pip install haystack-ai
pip install --upgrade pip
pip install farm-haystack[colab,faiss,inference]
pip install farm-haystack

# Below DocumentStore follows the Haystack example:
"Tutorial: Better Retrieval with Embedding Retrieval"
https://haystack.deepset.ai/tutorials/06_better_retrieval_via_embedding_retrieval
"""

import os
import json

from haystack import Document
# from haystack.document_stores.in_memory import InMemoryDocumentStore
# from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import EmbeddingRetriever, FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from haystack.schema import Document
from haystack.utils import print_answers

def create_document_store(squrl: str="sqlite:///wikitext.sqlite.db"):
    if squrl is None:
        # Write documents to InMemoryDocumentStore
        return InMemoryDocumentStore()

    return FAISSDocumentStore(sql_url=squrl, index="document")


def create_retriever(
    document_store, embed=True, top_k=5, use_gpu=False,
    embedding_model="jinaai/jina-embeddings-v2-base-en",
    HUGGINGFACE_TOKEN=None):

    if embed:
        return  EmbeddingRetriever(
            document_store=document_store,
            embedding_model=embedding_model,
            use_auth_token=HUGGINGFACE_TOKEN,
            use_gpu=use_gpu,
            # top_k=top_k  # Unsure if this works
        )

    return InMemoryBM25Retriever(
        document_store=document_store,
        top_k=top_k
    )

def json_to_document(json_fname: str):

    # Load JSON data
    with open(json_fname, "r") as file:
        data = json.load(file)
        documents = [
            Document(content=doc["content"], meta=doc.get("meta"))
            for doc in data
        ]

    return documents

def default_text_to_documents():
    return [
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


def ingest_documents(documents, document_store, retriever):
    # Write documents to the DocumentStore
    document_store.write_documents(documents)

    # Add embeddings to the documents in the DocumentStore
    document_store.update_embeddings(retriever)

    return document_store

""" # Section from FAISS example 
def config_reader(
        model_name_or_path="deepset/roberta-base-squad2",
        use_gpu=False):

    return FARMReader(
        model_name_or_path=model_name_or_path,
        use_gpu=use_gpu
    )
""" # End Section

# if __name__ == '__main__':
json_fname = "./excellent-articles/excellent-articles_10.json"
# json_fname = "dummy.json"
squrl = "sqlite:///wikitext.sqlite.db"
index = "document"
embed = True
top_k = 5  # Only use with InMemoryBM25Retriever
use_gpu=False
reader_model = "deepset/roberta-base-squad2"
embedding_model = "jinaai/jina-embeddings-v2-base-de"
HUGGINGFACE_TOKEN = os.environ.get('HUGGINGFACE_TOKEN')
# or userdata.get('HUGGINGFACE_TOKEN')

if os.path.exists(json_fname):
    documents = json_to_document(json_fname=json_fname)
else:
    documents = default_text_to_documents()

document_store = create_document_store(squrl='sqlite:///')

retriever = create_retriever(
    document_store,
    embed=embed,
    top_k=top_k,
    use_gpu=use_gpu,
    embedding_model=embedding_model,
    HUGGINGFACE_TOKEN=HUGGINGFACE_TOKEN
)

document_store = ingest_documents(
    documents=documents,
    document_store=document_store,
    retriever=retriever
)

# reader = config_reader(
#     model_name_or_path=reader_model,
#     use_gpu=use_gpu
# )

# pipe = ExtractiveQAPipeline(reader, retriever)

# prediction = pipe.run(
#     query="Who created the Dothraki vocabulary?",
#     params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}}
# )

# print("Predictions")
# print_answers(prediction, details="maximum")