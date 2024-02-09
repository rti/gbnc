# from haystack import Pipeline
from haystack import Document
from haystack.components.builders.answer_builder import AnswerBuilder

from .llm_config import llm
from .logger import get_logger
from .prompt import prompt_builders
from .vector_store_interface import embedder, retriever, input_documents

# Create logger instance from base logger config in `logger.py`
logger = get_logger(__name__)


def rag_pipeline(query: str = None, top_k: int = 3, lang: str = 'de'):

    assert (query is not None)

    if isinstance(query, str):
        query = Document(content=query)

    assert (isinstance(query, Document))

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

    answer_builder = AnswerBuilder()
    answer_build = answer_builder.run(
        query=query.content,  # As a Document class, .content returns the string
        replies=response['replies'],
        meta=response['meta'],
        documents=retriever_results['documents'],
        pattern=None,
        reference_pattern=None
    )

    logger.debug(f'{answer_build=}')

    return answer_build['answers'][0]
