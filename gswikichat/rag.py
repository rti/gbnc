
from haystack import Pipeline
from haystack.components.builders.answer_builder import AnswerBuilder

from .llm_config import llm
from .prompt import prompt_builder
from .vector_store_interface import retriever

answer_builder = AnswerBuilder()

rag_pipeline = Pipeline()
rag_pipeline.add_component("retriever", retriever)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("llm", llm)
rag_pipeline.add_component("answer_builder", answer_builder)

rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm")
rag_pipeline.connect("llm.replies", "answer_builder.replies")
rag_pipeline.connect("llm.metadata", "answer_builder.meta")
rag_pipeline.connect("retriever", "answer_builder.documents")
