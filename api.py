import os
import json

from haystack import Pipeline, Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack_integrations.components.generators.ollama import OllamaGenerator
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
llm = OllamaGenerator(model=os.getenv("MODEL"), url="http://localhost:11434/api/generate")
rag_pipeline = Pipeline()
rag_pipeline.add_component("retriever", retriever)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("llm", llm)
rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm")

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
        }
    )
    return results["llm"]["replies"]
