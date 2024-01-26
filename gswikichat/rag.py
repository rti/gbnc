import os

from haystack import Pipeline
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack_integrations.components.generators.ollama import OllamaGenerator
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.components.builders.prompt_builder import PromptBuilder

from .prompt import prompt_template
from .vector_store_interface import document_store


retriever = InMemoryBM25Retriever(
    document_store=document_store,
    top_k=1
)
prompt_builder = PromptBuilder(template=prompt_template)

print(f"Setting up ollama with {os.getenv('MODEL')}")
llm = OllamaGenerator(
    model=os.getenv("MODEL"),
    url="http://localhost:11434/api/generate"
)

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
