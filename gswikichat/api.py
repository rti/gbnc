from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

from .rag import answer_builder
from .llm_config import llm
from .prompt import prompt_builders
from .vector_store_interface import embedder, retriever, input_documents

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
    logger.debug(f'{top_k=}')

    query = Document(content=query)

    query_embedded = embedder.run([query])
    query_embedding = query_embedded['documents'][0].embedding

    retriever_results = retriever.run(
        query_embedding=list(query_embedding),
        filters=None,
        top_k=top_k,
        scale_score=None,
        return_embedding=None
    )

    logger.debug('retriever results:')
    for retriever_result_ in retriever_results:
        logger.debug(retriever_result_)

    prompt_builder = prompt_builders[lang]

    prompt_build = prompt_builder.run(
        question=query.content,  # As a Document instance, .content returns a string
        documents=retriever_results['documents']
    )

    prompt = prompt_build['prompt']

    logger.debug(f'{prompt=}')

    response = llm.run(prompt=prompt, generation_kwargs=None)

    answer_build = answer_builder.run(
        query=query.content,  # As a Document class, .content returns the string
        replies=response['replies'],
        meta=response['meta'],
        documents=retriever_results['documents'],
        pattern=None,
        reference_pattern=None
    )

    logger.debug(f'{answer_build=}')

    answer = answer_build['answers'][0]

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
