from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

from .rag import rag_pipeline


app = FastAPI()
app.mount("/frontend/dist", StaticFiles(directory="frontend/dist", html=True), name="frontend")


@app.get("/")
async def root():
    return RedirectResponse(url="/frontend/dist", status_code=302)


@app.get("/api")
async def api(q, topk=10):
    results = rag_pipeline.run(
        {
            "retriever": {"query": q, "top_k": topk},
            "prompt_builder": {"question": q},
            "answer_builder": {"query": q},
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
