ARG CUDA_VERSION="11.8.0"
ARG CUDNN_VERSION="8"
ARG UBUNTU_VERSION="22.04"
ARG DOCKER_FROM=nvidia/cuda:$CUDA_VERSION-cudnn$CUDNN_VERSION-devel-ubuntu$UBUNTU_VERSION

# Base NVidia CUDA Ubuntu image
FROM $DOCKER_FROM AS base

# Install Python plus openssh, which is our minimum set of required packages.
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get install -y --no-install-recommends openssh-server openssh-client git git-lfs && \
    python3 -m pip install --upgrade pip && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/local/cuda/bin:${PATH}"

# Install ollama llm inference engine
RUN curl https://ollama.ai/install.sh | sh

# Pull the language model
ARG MODEL=phi
ENV MODEL=${MODEL}
RUN ollama serve & while ! curl http://localhost:11434; do sleep 1; done; ollama pull $MODEL

# Install fastapi and web server
RUN pip install fastapi
RUN pip install "uvicorn[standard]"

# RAG framework haystack
RUN pip install haystack-ai
RUN pip install ollama-haystack

# Container start script
COPY --chmod=755 start.sh /start.sh

# Setup the custom API and frontend
WORKDIR /workspace
COPY --chmod=644 api.py /workspace/
COPY --chmod=755 static /workspace/static

CMD [ "/start.sh" ]
