import os
import json

from haystack import Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever

# TODO: FAISS: Facebook AI Similarity Search
# from haystack.nodes import Seq2SeqGenerator
# from haystack.utils import convert_files_to_dicts, fetch_archive_from_http, clean_wiki_text
# from haystack.nodes import EmbeddingRetriever, DensePassageRetriever
# from haystack.document_stores.faiss import FAISSDocumentStore

# document_store = FAISSDocumentStore(
#     faiss_index_factory_str="Flat", vector_dim=128)

# retriever = EmbeddingRetriever(document_store=document_store,
#                                embedding_model="yjernite/retribert-base-uncased", model_format="retribert")

# document_store.delete_documents()
# # document_store.save("my_faiss_index.faiss")
# new_document_store = FAISSDocumentStore.load("my_faiss_index.faiss")

top_k = 5
documents = []

if os.path.isfile("./excellent-articles/excellent-articles.json"):
    with open("./excellent-articles/excellent-articles.json", 'r') as f:
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
