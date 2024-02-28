import os

from typing import Annotated

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Header

from .logger import get_logger
from .rag import rag_pipeline

# Create logger instance from base logger config in `logger.py`
logger = get_logger(__name__)

FRONTEND_STATIC_DIR = "./frontend/dist"
API_SECRET = os.environ.get("API_SECRET")

app = FastAPI()

app.mount(
    "/assets",
    StaticFiles(directory=f"{FRONTEND_STATIC_DIR}/assets"),
    name="frontend-assets",
)


@app.get("/")
async def root():
    return FileResponse(f"{FRONTEND_STATIC_DIR}/index.html")


@app.get("/favicon.ico")
async def favicon():
    return FileResponse(f"{FRONTEND_STATIC_DIR}/favicon.ico")


@app.get("/api")
async def api(x_api_secret: Annotated[str, Header()], query, top_k=3, lang='en'):
    if not API_SECRET == x_api_secret:
        raise Exception("API key is missing or incorrect") 

    if not lang in ["en", "de"]:
        raise Exception("language must be 'en' or 'de'")

    logger.debug(f"{query=}")
    logger.debug(f"{top_k=}")
    logger.debug(f"{lang=}")

    answer = rag_pipeline(query=query, top_k=top_k, lang=lang)

    if not answer:
        return {}

    sources = [
        {"id": d_.id, "source": d_.meta["source"], "content": d_.content, "score": d_.score}
        for d_ in answer.documents
    ]

    logger.debug(f"{answer.data=}")
    logger.debug(f"{answer.documents=}")

    return {"answer": answer.data.content, "sources": sources}
