import os
import json

from haystack import Document, Pipeline
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.writers import DocumentWriter

top_k = 5
input_documents = []

if os.path.isfile("./json_input/excellent-articles.json"):
    with open("./json_input/excellent-articles.json", 'r') as f:
        json_obj = json.load(f)
        for k, v in json_obj.items():
            print(f"Loading {k}")
            input_documents.append(Document(content=v, meta={"src": k}))
else:
    input_documents = [
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
document_store = InMemoryDocumentStore(embedding_similarity_function="cosine")
# document_store.write_documents(input_documents)


embedder = SentenceTransformersDocumentEmbedder(
    model="sentence-transformers/all-MiniLM-L6-v2"
)
embedder.warm_up()

documents_with_embeddings = embedder.run(input_documents)
document_store.write_documents(documents_with_embeddings['documents'])

retriever = InMemoryEmbeddingRetriever(
    # embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    document_store=document_store,
    top_k=top_k
)

# writer = DocumentWriter(document_store=document_store)

# indexing_pipeline = Pipeline()
# indexing_pipeline.add_component("embedder", embedder)
# indexing_pipeline.add_component("writer", writer)
# indexing_pipeline.connect("embedder", "writer")
# indexing_pipeline.run(
#     {
#         "embedder": {"documents": input_documents}
#     }
# )
