import os

# from haystack import Pipeline
# from haystack.pipelines import Pipeline
# from haystack_integrations.components.generators.ollama import OllamaGenerator
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack import Pipeline


from .prompt import prompt_builder
from .llm_config import llm
from .vector_store_interface import retriever

""" Section from FAISS Example """
# pipeline = DocumentSearchPipeline(retriever)

# # Example query
# results = pipeline.run(
#     query="Your search query",
#     params={"Retriever": {"top_k": 10}}
# )

# for result in results["documents"]:
#     title = result.meta['title'] if 'title' in result.meta else 'No title'

#     print(f"Title: {title}")
#     print(f"Content: {result.content}")
#     print("-----")
""" End Section from FAISS Example """

answer_builder = AnswerBuilder()

rag_pipeline = Pipeline()
# rag_pipeline = DocumentSearchPipeline(retriever)
rag_pipeline.add_component("retriever", retriever)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("llm", llm)
rag_pipeline.add_component("answer_builder", answer_builder)

rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm")
rag_pipeline.connect("llm.replies", "answer_builder.replies")
rag_pipeline.connect("llm.metadata", "answer_builder.meta")
rag_pipeline.connect("retriever", "answer_builder.documents")
