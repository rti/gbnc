from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

# from .rag import rag_pipeline
from .rag import embedder, retriever, prompt_builder, llm, answer_builder
from haystack import Document


app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.get("/")
async def root():
    return RedirectResponse(url="/static", status_code=302)


@app.get("/api")
async def api(q):

    embedder, retriever, prompt_builder, llm, answer_builder

    # query = "How many languages are there?"
    query = Document(content=q)

    result = embedder.run([query])

    # print(help(retriever))
    results = retriever.run(
        query_embedding=result['documents'][0].embedding,
        filters=None,
        top_k=None,
        scale_score=None,
        return_embedding=None
    )
    # .run(
    #     result['documents'][0].embedding
    # )

    prompt = prompt_builder.run(documents=results['documents'])['prompt']

    response = llm.run(prompt=prompt, generation_kwargs=None)
    # reply = response['replies'][0]

    # rag_pipeline.connect("llm.replies", "answer_builder.replies")
    # rag_pipeline.connect("llm.metadata", "answer_builder.meta")
    # rag_pipeline.connect("retriever", "answer_builder.documents")

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
