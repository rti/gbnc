import os
import json

from tqdm import tqdm
from pprint import pprint

from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import JSONLoader
from langchain_community.embeddings.fake import FakeEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

import torch

from .logger import get_logger

# Create logger instance from base logger config in `logger.py`
logger = get_logger(__name__)

HUGGING_FACE_HUB_TOKEN = os.environ.get('HUGGING_FACE_HUB_TOKEN')

# disable this line to disable the embedding cache
EMBEDDING_CACHE_FILE = '/root/.cache/gbnc_embeddings.json'

top_k = 5
input_documents = []

device = "cpu"

if torch.cuda.is_available():
    logger.info('GPU is available.')
    device = "cuda"


# TODO: Add the json strings as env variables
json_dir = 'json_input'
json_fname = 'data.json'

json_fpath = os.path.join(json_dir, json_fname)

def metadata_func(record: dict, metadata: dict) -> dict:
    metadata["source"] = record.get("meta").get("source")
    return metadata

# Create the JSONLoader instance
loader = JSONLoader(
    file_path=json_fpath,
    jq_schema='.[]',
    content_key="content",
    metadata_func=metadata_func
)

documents = loader.load()
pprint(documents[0])

text_splitter = CharacterTextSplitter(chunk_size=250, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# https://huggingface.co/svalabs/german-gpl-adapted-covid
sentence_transformer_model = 'svalabs/german-gpl-adapted-covid'
logger.info(f'Sentence Transformer Name: {sentence_transformer_model}')

embeddings = HuggingFaceEmbeddings(
    model_name=sentence_transformer_model,
    model_kwargs={'device': device},
    show_progress=True,
)

from langchain_community.vectorstores.pgvecto_rs import PGVecto_rs

import os

PORT = os.getenv("DB_PORT", 5432)
HOST = os.getenv("DB_HOST", "127.0.0.1")
USER = os.getenv("DB_USER", "gbnc")
PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "gbnc")


URL = "postgresql+psycopg://{username}:{password}@{host}:{port}/{db_name}".format(
    port=PORT,
    host=HOST,
    username=USER,
    password=PASS,
    db_name=DB_NAME,
)


logger.info(f"Inserting {len(docs)} documents")

db = PGVecto_rs.from_documents(
    documents=docs,
    embedding=embeddings,
    db_url=URL,
    collection_name="gbnc",
)

logger.info('done')
