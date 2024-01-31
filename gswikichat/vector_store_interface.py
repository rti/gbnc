import os
import json

from haystack import Document, Pipeline
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.writers import DocumentWriter
from haystack.document_stores.types.policy import DuplicatePolicy

top_k = 5
input_documents = []

json_dir = 'json_input'
json_fname = 'excellent-articles_10_paragraphs.json'
json_fpath = os.path.join(json_dir, json_fname)

if os.path.isfile(json_fpath):
    with open(json_fpath, 'r') as finn:
        json_obj = json.load(finn)

    if isinstance(json_obj, dict):
        for k, v in json_obj.items():
            print(f"Loading {k}")
            input_documents.append(Document(content=v, meta={"src": k}))
    elif isinstance(json_obj, list):
        for obj_ in json_obj:
            url = obj_['meta']
            content = obj_['content']

            input_documents.append(
                Document(
                    content=content,
                    meta={'src': url}
                )
            )
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

document_store = InMemoryDocumentStore(
    embedding_similarity_function="cosine",
    # embedding_dim=768,
    # duplicate_documents="overwrite"
)
# document_store.write_documents(input_documents)

# TODO Introduce Jina.AI from HuggingFace. Establish env-variable for trust_...
embedder = SentenceTransformersDocumentEmbedder(
    # model="sentence-transformers/all-MiniLM-L6-v2",
    model="jinaai/jina-embeddings-v2-base-de",
    token='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'
)

embedder.warm_up()

documents_with_embeddings = embedder.run(input_documents)

document_store.write_documents(
    documents=documents_with_embeddings['documents'],
    policy=DuplicatePolicy.OVERWRITE
)

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
