from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

from .rag import rag_pipeline

from haystack import Document
from .logger import get_logger

# Create logger instance from base logger config in `logger.py`
logger = get_logger(__name__)

FRONTEND_STATIC_DIR = './frontend/dist'

app = FastAPI()

app.mount(
    "/assets",
    StaticFiles(directory=f"{FRONTEND_STATIC_DIR}/assets"),
    name="frontend-assets"
)

@app.get("/")
async def root():
    return FileResponse(f"{FRONTEND_STATIC_DIR}/index.html")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(f"{FRONTEND_STATIC_DIR}/favicon.ico")

@app.get("/api")
async def api(query, top_k=3, lang='en'):
    if not lang in ['en', 'de']:
        raise Exception("language must be 'en' or 'de'")

    logger.debug(f'{query=}')  # Assuming we change the input name
    logger.debug(f'{top_k=}')
    logger.debug(f'{lang=}')

    answer = rag_pipeline(
        query=query,
        top_k=top_k,
        lang=lang
    )

    sources = [
        {
            "src": d_.meta['source'],
            "content": d_.content,
            "score": d_.score
        } for d_ in answer.documents
    ]

    logger.debug(f'{answer=}')

    return {
        "answer": answer.data.content,
        "sources": sources
    }
