from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

from .rag import embedder, retriever, prompt_builder, llm, answer_builder
from haystack import Document


app = FastAPI()
app.mount(
    "/frontend/dist",
    StaticFiles(directory="frontend/dist", html=True),
    name="frontend"
)


@app.get("/")
async def root():
    return RedirectResponse(url="/frontend/dist", status_code=302)


@app.get("/api")
async def api(q):

    query = Document(content=q)

    result = embedder.run([query])

    results = retriever.run(
        query_embedding=list(result['documents'][0].embedding),
        filters=None,
        top_k=None,
        scale_score=None,
        return_embedding=None
    )

    prompt = prompt_builder.run(documents=results['documents'])['prompt']

    response = llm.run(prompt=prompt, generation_kwargs=None)


    results = answer_builder.run(
        query=q,
        replies=response['replies'],
        meta=response['meta'],
        documents=results['documents'],
        pattern=None,
        reference_pattern=None
    )

    answer = results['answers'][0]

    return {
        "answer": answer.data,
        "sources": [{
            "src": d.meta['src'],
            "content": d.content,
            "score": d.score
        } for d in answer.documents]
    }
