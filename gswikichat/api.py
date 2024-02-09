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
    # return RedirectResponse(url="/frontend/dist", status_code=308)
    return {}


@app.get("/api")
async def api(q, top_k = 3, lang = 'en'):
    if not lang in ['en', 'de']:
        raise Exception("language must be 'en' or 'de'") 

    print(f"{q=}")
    print(f"{top_k=}")
    print(f"{lang=}")

    query = Document(content=q)

    queryEmbedded = embedder.run([query])
    queryEmbedding = queryEmbedded['documents'][0].embedding

    retrieverResults = retriever.run(
        query_embedding=list(queryEmbedding),
        filters=None,
        top_k=top_k,
        scale_score=None,
        return_embedding=None
    )

    print("retriever results:")
    for retrieverResult in retrieverResults:
        print(retrieverResult)

    promptBuilder = prompt_builder[lang] 
    promptBuild = promptBuilder.run(question=q, documents=retrieverResults['documents'])
    prompt = promptBuild['prompt']

    print(f"{prompt=}")

    response = llm.run(prompt=prompt, generation_kwargs=None)

    answerBuild = answer_builder.run(
        query=q,
        replies=response['replies'],
        meta=response['meta'],
        documents=retrieverResults['documents'],
        pattern=None,
        reference_pattern=None
    )
    print("answerBuild", answerBuild)

    answer = answerBuild['answers'][0]

    sources= [{ "src": d.meta['src'], "content": d.content, "score": d.score } for d in answer.documents]

    print("answer", answer)

    return {
        "answer": answer.data,
        "sources": sources
    }
