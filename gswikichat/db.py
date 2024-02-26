import os

import torch

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import JSONLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.pgvecto_rs import PGVecto_rs

from .logger import get_logger


SENTENCE_TRANSFORMER_MODEL = "svalabs/german-gpl-adapted-covid"

logger = get_logger(__name__)


def get_device():
    device = "cpu"
    if torch.cuda.is_available():
        logger.info("GPU is available.")
        device = "cuda"
    return device


def get_embedding_model():
    # https://huggingface.co/svalabs/german-gpl-adapted-covid
    logger.info(f"Embedding model: {SENTENCE_TRANSFORMER_MODEL}")

    return HuggingFaceEmbeddings(
        model_name=SENTENCE_TRANSFORMER_MODEL,
        model_kwargs={"device": get_device()},
        show_progress=True,
    )


def get_db():
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

    return PGVecto_rs.from_collection_name(
        embedding=get_embedding_model(),
        db_url=URL,
        collection_name="gbnc",
    )


def import_data(file):
    def metadata_func(record: dict, metadata: dict) -> dict:
        metadata["source"] = record.get("meta", {}).get("source")
        return metadata

    loader = JSONLoader(
        file_path=file,
        jq_schema=".[]",
        content_key="content",
        metadata_func=metadata_func,
    )

    documents = loader.load()

    logger.debug(f"Loaded {len(documents)} documents.")

    text_splitter = CharacterTextSplitter(chunk_size=250, chunk_overlap=0)
    chunks = text_splitter.split_documents(documents)
    logger.debug(f"Split documents into {len(chunks)} chunks.")

    logger.debug(f"Importing into database.")
    get_db().add_documents(chunks)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        file = sys.argv[1]
        import_data(file)

    else:
        logger.error(
            """Provide JSON file with the following structure as first parameter
    [
        {
            "content":"document content one", "meta":{
                "source": "https://source.url/one"
            }
        },
        {
            "content":"document content two", "meta":{
                "source": "https://source.url/two"
            }
        }
    ]
            """
        )
        sys.exit(1)
