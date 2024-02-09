
from haystack import Pipeline
from haystack.components.builders.answer_builder import AnswerBuilder

answer_builder = AnswerBuilder()

# rag_pipeline = Pipeline()
# rag_pipeline.add_component("text_embedder", embedder)
# rag_pipeline.add_component("retriever", retriever)
# # rag_pipeline.add_component("writer", writer)
# rag_pipeline.add_component("prompt_builder", prompt_builder)
# rag_pipeline.add_component("llm", llm)
# rag_pipeline.add_component("answer_builder", answer_builder)

# # rag_pipeline.connect("embedder", "writer")
# rag_pipeline.connect("retriever.documents", "text_embedder")
# rag_pipeline.connect("retriever", "prompt_builder.documents")
# rag_pipeline.connect("prompt_builder", "llm")
# rag_pipeline.connect("llm.replies", "answer_builder.replies")
# rag_pipeline.connect("llm.metadata", "answer_builder.meta")
# rag_pipeline.connect("retriever", "answer_builder.documents")

# rag_pipeline.run(
#     {
#         "text_embedder": {"documents": input_documents}
#     }
# )
