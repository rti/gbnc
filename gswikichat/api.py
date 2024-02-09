from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

from .rag import rag_pipeline

from haystack import Document
from .logger import get_logger

# Create logger instance from base logger config in `logger.py`
logger = get_logger(__name__)

STATIC_DIR = 'frontend/dist'
LANDING_PAGE = f'/{STATIC_DIR}'

app = FastAPI()
app.mount(
    LANDING_PAGE,
    StaticFiles(directory=STATIC_DIR, html=True),
    name="frontend"
)


@app.get("/")
async def root():
    return RedirectResponse(
        url=LANDING_PAGE,
        status_code=308
    )
    # return {}


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
            "src": d_.meta['src'],
            "content": d_.content,
            "score": d_.score
        } for d_ in answer.documents
    ]

    logger.debug(f'{answer=}')

    return {
        "answer": answer.data,
        "sources": sources
    }
