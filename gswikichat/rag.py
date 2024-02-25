# from haystack import Pipeline
from haystack import Document
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.dataclasses import ChatMessage

from .llm_config import llm
from .logger import get_logger
from .prompt import user_prompt_builders, system_prompts
from .vector_store_interface import db

# Create logger instance from base logger config in `logger.py`
logger = get_logger(__name__)


def rag_pipeline(query: str, top_k: int = 3, lang: str = 'de'):

    docs_with_score = db.similarity_search_with_score(query, top_k)

    for doc, score in docs_with_score:
        print("-" * 80)
        print("Score: ", score)
        print(doc.page_content)
        print("-" * 80)

    # langchain doc to haystack doc
    docs = [Document.from_dict({"content":d.page_content,"meta":d.metadata}) for d,_ in docs_with_score]

    system_prompt = system_prompts[lang]
    user_prompt_builder = user_prompt_builders[lang]

    user_prompt_build = user_prompt_builder.run(
        question=query,
        documents=docs
    )

    prompt = user_prompt_build['prompt']

    logger.debug(f'{prompt=}')

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
        query=query_document.content,
        replies=response['replies'],
        meta=[r.meta for r in response['replies']],
        documents=retriever_results['documents'],
        pattern=None,
        reference_pattern=None
    )

    logger.debug(f'{answer_build=}')

    return answer_build['answers'][0]
