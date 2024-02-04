# Naïve Infrastructure for a GB&C project

**Warning** This is a prototype for development only. No security considerations have been made. All services run as root!

## Getting started

### Locally

To build and run the container locally with hot reload on python files do:
```
DOCKER_BUILDKIT=1 docker build . -t gbnc
docker run  \
  -v "$(pwd)/gswikichat":/workspace/gswikichat \
  -v "$(pwd)/cache":/root/.cache \
  -e HUGGING_FACE_HUB_TOKEN=$HUGGING_FACE_HUB_TOKEN
  -p 8000:8000 \
  --rm -it \
  --name gbnc \
  gbnc
```
Point your browser to http://localhost:8000/ and use the frontend.

### Runpod.io

The container works on [runpod.io](https://www.runpod.io/) GPU instances. A [template is available here](https://runpod.io/gsc?template=0w8z55rf19&ref=yfvyfa0s).

### Local development
#### Backend
```
python -m venv .venv
. ./.venv/bin/activate
pip install -r requirements.txt
```
#### Frontend
```
cd frontend
yarn dev
```

## What's in the box

### Docker container

One container running all the components. No separation to keep it simple. Based on [Nvidia CUDA containers](https://hub.docker.com/r/nvidia/cuda) in order to support GPU acceleration. Small models work on laptop CPUs too (tested i7-1260P).

### Ollama inference

The container runs [Ollama](https://ollama.ai/) for LLM inference. Will probably not scale enough when run as a service for multiple users, but enough for testing.

### Phi2 LLM

The [Microsoft Phi2 2.7B](https://www.microsoft.com/en-us/research/blog/phi-2-the-surprising-power-of-small-language-models/) model is run by default. The model runs locally using Ollama. Can be switched with the `MODEL` docker build arg.

### Haystack RAG Framework

The [Haystack RAG framework](https://haystack.deepset.ai/) is used to implement Retrieval Augmented Generation on a minimal test dataset.

### API

A [FastAPI](https://fastapi.tiangolo.com/) server is running in the container. It exposes an API to receive a question from the frontend, runs the Haystack RAG and returns the response.

### Frontend

A minimal frontend lets the user input a question and renders the response from the system.

## Sentence Transformers Statistics

```
basic_transformer_models = [
    "all-MiniLM-L6-v2",
    "xlm-clm-ende-1024",
    "xlm-mlm-ende-1024",
    "bert-base-german-cased",
    "bert-base-german-dbmdz-cased",
    "bert-base-german-dbmdz-uncased",
    "distilbert-base-german-cased",
    "xlm-roberta-large-finetuned-conll03-german",
    "deutsche-telekom/gbert-large-paraphrase-cosine"
]

https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
sentence_transformer_model = "all-MiniLM-L6-v2"
3 minutes to batch 82

https://huggingface.co/deutsche-telekom/gbert-large-paraphrase-cosine
sentence_transformer_model = 'deutsche-telekom/gbert-large-paraphrase-cosine'
76 minutes to batch 82

https://huggingface.co/jinaai/jina-embeddings-v2-base-de
sentence_transformer_model = 'jinaai/jina-embeddings-v2-base-de'
Cannot find or load the embedding model
Unknown minutes to batch 82

https://huggingface.co/aari1995/German_Semantic_STS_V2
sentence_transformer_model = 'aari1995/German_Semantic_STS_V2'
75 minutes to batch 82

https://huggingface.co/Sahajtomar/German-semantic
sentence_transformer_model = 'Sahajtomar/German-semantic'
72 minutes to batch 82

https://huggingface.co/svalabs/german-gpl-adapted-covid
ntence_transformer_model = 'svalabs/german-gpl-adapted-covid'
2 minutes to batch 82

https://huggingface.co/PM-AI/bi-encoder_msmarco_bert-base_german
sentence_transformer_model = 'PM-AI/bi-encoder_msmarco_bert-base_german'
14 minutes to batch 82

https://huggingface.co/JoBeer/german-semantic-base
sentence_transformer_model = 'JoBeer/german-semantic-base'
22 minutes to batch 82
```
