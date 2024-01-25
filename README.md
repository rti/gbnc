# Naïve Infrastructure for a GB&C project

## What's in the box

### Docker container

One container running all the components at the moment. No separation to keep it simple. Based on [Nvidia CUDA containers](https://hub.docker.com/r/nvidia/cuda) in order to support GPU acceleration. Small models work on laptop CPUs too.

### Ollama inference

The docker container runs an [Ollama](https://ollama.ai/) for LLM inference. Will probably not scale enough when run as a service for multiple users, but enough for testing right now.

### Phi2 LLM

For now the [Microsoft Phi2 2.7B](https://www.microsoft.com/en-us/research/blog/phi-2-the-surprising-power-of-small-language-models/) model is run used by default. The model runs locally using Ollama.

### Haystack RAG Framework

The [Haystack RAG framework](https://haystack.deepset.ai/) is used to implement Retrieval Augmented Generation on a minimal test dataset.

### A trivial API

A [FastAPI](https://fastapi.tiangolo.com/) server is running in the container. It exposes a simple API to receive a question from the frontend, runs the Haystack RAG and returns the response.

### Minimal frontend

A minimal frontend lets the user input a question and renders the response from the system.


## How to run

### Locally

To build and run the container locally do:
```
docker build . -t gbnc
docker run -p 8000:8000 --rm -it gbnc
```
Now you can point your browser to http://localhost:8000/ and use the frontend.

### Runpod.io

The container was tested on a [runpod.io](https://www.runpod.io/) GPU instance. A [template is available here](https://runpod.io/gsc?template=0w8z55rf19&ref=yfvyfa0s).
