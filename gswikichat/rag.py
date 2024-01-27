import os

from haystack.nodes import PreProcessor, EmbeddingRetriever
from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines import Pipeline
from haystack.schema import Document

# from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack_integrations.components.generators.ollama import OllamaGenerator
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.components.builders.prompt_builder import PromptBuilder

from .prompt import prompt_template
# from .vector_store_interface import document_store

HUGGINGFACE_TOKEN = os.environ.get('HUGGINGFACE_TOKEN')

document_store = InMemoryDocumentStore(embedding_dim=384)
preprocessor = PreProcessor()
retriever = EmbeddingRetriever(
    embedding_model="jinaai/jina-embeddings-v2-base-de",
    use_auth_token=HUGGINGFACE_TOKEN,
    document_store=document_store
)

prompt_builder = PromptBuilder(template=prompt_template)

# TODO: discolm prompt https://huggingface.co/DiscoResearch/DiscoLM_German_7b_v1
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


indexing_pipeline = Pipeline()
indexing_pipeline.add_node(component=preprocessor,
                           name="Preprocessor", inputs=["File"])
indexing_pipeline.add_node(
    component=retriever, name="Retriever", inputs=["Preprocessor"])
indexing_pipeline.add_node(component=document_store,
                           name="document_store", inputs=["Retriever"])
indexing_pipeline.run(documents=[Document("This is my document")])
