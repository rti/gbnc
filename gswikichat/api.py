from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

from .rag import answer_builder
from .llm_config import llm
from .prompt import prompt_builders
from .vector_store_interface import embedder, retriever, input_documents

from haystack import Document

import logging
import sys

# TODO: Test if this can be added to the `__init__.py` file
# TODO: Add volume to Dockerfile for `gbnc_api.log` file
# Source: https://docs.python.org/3/howto/logging.html
logging.basicConfig(
    filename='gbnc_api.log',
    encoding='utf-8',
    level=logging.DEBUG
)

# Source: https://stackoverflow.com/questions/14058453/
# making-python-loggers-output-all-messages-to-stdout-in-addition-to-log-file
logger = logging.getLogger('gswikicat api')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
# End of logging logger configuration


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
