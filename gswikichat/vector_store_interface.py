import os
import json

# from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from haystack import Document  # , Pipeline
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
# from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.document_stores.in_memory import InMemoryDocumentStore
# from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
# from haystack.components.writers import DocumentWriter
from haystack.document_stores.types.policy import DuplicatePolicy

HUGGING_FACE_HUB_TOKEN = os.environ.get('HUGGING_FACE_HUB_TOKEN')
top_k = 5
input_documents = []

json_dir = 'json_input'
json_fname = 'excellent-articles_10_paragraphs.json'
json_fpath = os.path.join(json_dir, json_fname)

if os.path.isfile(json_fpath):
    print(f'[INFO] Loading data from {json_fpath}')
    with open(json_fpath, 'r') as finn:
        json_obj = json.load(finn)

    if isinstance(json_obj, dict):
        for k, v in tqdm(json_obj.items()):
            print(f"Loading {k}")
            input_documents.append(Document(content=v, meta={"src": k}))
    elif isinstance(json_obj, list):
        for obj_ in tqdm(json_obj):
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

# basic_transformer_models = [
#     "all-MiniLM-L6-v2",
#     "xlm-clm-ende-1024",
#     "xlm-mlm-ende-1024",
#     "bert-base-german-cased",
#     "bert-base-german-dbmdz-cased",
#     "bert-base-german-dbmdz-uncased",
#     "distilbert-base-german-cased",
#     "xlm-roberta-large-finetuned-conll03-german",
#     "deutsche-telekom/gbert-large-paraphrase-cosine"
# ]

# https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
# sentence_transformer_model = "all-MiniLM-L6-v2"
# 3 minutes to batch 82

# https://huggingface.co/deutsche-telekom/gbert-large-paraphrase-cosine
# sentence_transformer_model = 'deutsche-telekom/gbert-large-paraphrase-cosine'
# 76 minutes to batch 82

# https://huggingface.co/jinaai/jina-embeddings-v2-base-de
# sentence_transformer_model = 'jinaai/jina-embeddings-v2-base-de'
# Cannot find or load the embedding model
# Unknown minutes to batch 82

# https://huggingface.co/aari1995/German_Semantic_STS_V2
# sentence_transformer_model = 'aari1995/German_Semantic_STS_V2'
# 75 minutes to batch 82

# https://huggingface.co/Sahajtomar/German-semantic
# sentence_transformer_model = 'Sahajtomar/German-semantic'
# 72 minutes to batch 82

# https://huggingface.co/svalabs/german-gpl-adapted-covid
sentence_transformer_model = 'svalabs/german-gpl-adapted-covid'
# 2 minutes to batch 82

# https://huggingface.co/PM-AI/bi-encoder_msmarco_bert-base_german
# sentence_transformer_model = 'PM-AI/bi-encoder_msmarco_bert-base_german'
# 14 minutes to batch 82

# https://huggingface.co/JoBeer/german-semantic-base
# sentence_transformer_model = 'JoBeer/german-semantic-base'
# 22 minutes to batch 82

print(f'Sentence Transformer Name:{sentence_transformer_model}')

embedder = SentenceTransformersDocumentEmbedder(
    model=sentence_transformer_model,
    # model="T-Systems-onsite/german-roberta-sentence-transformer-v2",
    # model="jinaai/jina-embeddings-v2-base-de",
    # token=HUGGING_FACE_HUB_TOKEN
)

# hg_embedder = SentenceTransformer(
#     "jinaai/jina-embeddings-v2-base-de",
#     token=HUGGING_FACE_HUB_TOKEN
# )

embedder.warm_up()

documents_with_embeddings = embedder.run(input_documents)
# documents_with_embeddings = embedder.encode(input_documents)


# print('\n\n')
# # print(documents_with_embeddings['documents'])
# print(type(documents_with_embeddings['documents']))
# print(len(documents_with_embeddings['documents']))
# print(dir(documents_with_embeddings['documents'][0]))
# print('\n\n')
# print(type(embedder.model))
# print('\n\n')
# # print(dir(hg_embedder))


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
