# from haystack import Pipeline
from haystack import Document
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.dataclasses import ChatMessage

from .db import get_db
from .llm_config import llm
from .logger import get_logger
from .prompt import user_prompt_builders, system_prompts

# Create logger instance from base logger config in `logger.py`
logger = get_logger(__name__)


def langchain_to_haystack_doc(langchain_document, score):
    return Document.from_dict(
        {
            "content": langchain_document.page_content,
            "meta": langchain_document.metadata,
            "score": score,
        }
    )


def rag_pipeline(query: str, top_k: int, lang: str):
    docs_with_score = get_db().similarity_search_with_score(query, top_k)
    docs_with_score.reverse() # best first

    if len(docs_with_score) == 0:
        return None

    logger.debug("Matching documents: ")
    for doc, score in docs_with_score:
        logger.debug("-" * 80)
        logger.debug(f"Score: {score}")
        logger.debug(doc.page_content)

    docs = [langchain_to_haystack_doc(d, s) for d, s in docs_with_score]

    system_prompt = system_prompts[lang]
    user_prompt_builder = user_prompt_builders[lang]
    user_prompt_build = user_prompt_builder.run(question=query, documents=docs)
    prompt = user_prompt_build["prompt"]

    logger.debug(f"{prompt=}")

    messages = [
        ChatMessage.from_system(system_prompt),
        ChatMessage.from_user(prompt),
    ]

    response = llm.run(
        messages,
        # generation_kwargs={"temperature": 0.2}
    )

    logger.debug(response)

    answer_builder = AnswerBuilder()
    answer_build = answer_builder.run(
        query=query,
        replies=response["replies"],
        meta=[r.meta for r in response["replies"]],
        documents=docs,
        pattern=None,
        reference_pattern=None,
    )

    logger.debug(f"{answer_build=}")

    return answer_build["answers"][0]
