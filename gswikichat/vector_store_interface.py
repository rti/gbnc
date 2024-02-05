import os
import json

from tqdm import tqdm

from haystack import Document  # , Pipeline
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.document_stores.types.policy import DuplicatePolicy
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.preprocessors import DocumentCleaner

HUGGING_FACE_HUB_TOKEN = os.environ.get('HUGGING_FACE_HUB_TOKEN')
EMBEDDING_CACHE_FILE = '/tmp/gbnc_embeddings.json'

top_k = 5
input_documents = []

json_dir = 'json_input'
json_fname = 'excellent-articles_10.json'

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

# cleaner = DocumentCleaner(
#         remove_empty_lines=True,
#         remove_extra_whitespaces=True,
#         remove_repeated_substrings=False)
# input_documents = cleaner.run(input_documents)['documents']

splitter = DocumentSplitter(split_by="sentence", split_length=5, split_overlap=0)
input_documents = splitter.run(input_documents)['documents']

document_store = InMemoryDocumentStore(
    embedding_similarity_function="cosine",
    # embedding_dim=768,
    # duplicate_documents="overwrite"
)

# https://huggingface.co/svalabs/german-gpl-adapted-covid
sentence_transformer_model = 'svalabs/german-gpl-adapted-covid'
print(f'Sentence Transformer Name: {sentence_transformer_model}')

embedder = SentenceTransformersDocumentEmbedder(
    model=sentence_transformer_model,
)
embedder.warm_up()


# if os.path.isfile(EMBEDDING_CACHE_FILE):
#     print("[INFO] Loading embeddings from cache")
#
#     with open(EMBEDDING_CACHE_FILE, 'r') as f:
#         documentsDict = json.load(f)
#         document_store.write_documents(
#             documents=[Document.from_dict(d) for d in documentsDict],
#             policy=DuplicatePolicy.OVERWRITE
#         )
#
# else:
if True:
    embedded = embedder.run(input_documents)
    document_store.write_documents(
        documents=embedded['documents'],
        policy=DuplicatePolicy.OVERWRITE
    )

    with open(EMBEDDING_CACHE_FILE, 'w') as f:
        documentsDict = [Document.to_dict(d) for d in embedded['documents']]
        json.dump(documentsDict, f)

retriever = InMemoryEmbeddingRetriever(document_store=document_store)

