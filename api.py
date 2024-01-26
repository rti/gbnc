import os
import json

from haystack import Pipeline, Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack_integrations.components.generators.ollama import OllamaGenerator
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.components.builders.prompt_builder import PromptBuilder

documents = []

if os.path.isfile("./excellent-articles/excellent-articles.json"):
    with open("./excellent-articles/excellent-articles.json", 'r') as f:
        json_obj = json.load(f)
        for k, v in json_obj.items():
            print(f"Loading {k}")
            documents.append(Document(content=v, meta={"src": k}))
else:
    documents = [
            Document(content="My name is Asra, I live in Paris.", meta={"src": "doc_1"}),
            Document(content="My name is Lee, I live in Berlin.", meta={"src": "doc2"}),
            Document(content="My name is Giorgio, I live in Rome.", meta={"src": "doc_3"}),
        ]

# Write documents to InMemoryDocumentStore
document_store = InMemoryDocumentStore()
document_store.write_documents(documents) 

# TODO: discolm prompt https://huggingface.co/DiscoResearch/DiscoLM_German_7b_v1
prompt_template = """
Given these documents, answer the question. Answer in a full sentence. Give the response only, no explanation. Don't mention the documents.
Documents:
{% for doc in documents %}
    {{ doc.content }}
{% endfor %}
Question: {{question}}
Answer:
"""

retriever = InMemoryBM25Retriever(document_store=document_store)
prompt_builder = PromptBuilder(template=prompt_template)
print(f"Setting up ollama with {os.getenv('MODEL')}")
llm = OllamaGenerator(model=os.getenv("MODEL"), url="http://localhost:11434/api/generate")
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

# =============================================================================

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()
app.mount("/app", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return RedirectResponse(url="/app/index.html", status_code=302)

@app.get("/api")
async def api(q):
    results = rag_pipeline.run(
        {
            "retriever": {"query": q },
            "prompt_builder": {"question": q },
            "answer_builder": {"query": q },
        }
    )
    answer = results["answer_builder"]["answers"][0]
    return {
            "answer": answer.data,
            "sources": [{
                "src": d.meta["src"],
                "content": d.content,
                "score": d.score
                } for d in answer.documents]
            }
