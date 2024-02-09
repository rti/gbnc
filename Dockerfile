ARG CUDA_VERSION="11.8.0"
ARG CUDNN_VERSION="8"
ARG UBUNTU_VERSION="22.04"
ARG CUDA_FROM=nvidia/cuda:$CUDA_VERSION-cudnn$CUDNN_VERSION-devel-ubuntu$UBUNTU_VERSION

ARG OLLAMA_VERSION="0.1.22"
ARG OLLAMA_FROM=ollama/ollama:$OLLAMA_VERSION
FROM $OLLAMA_FROM as ollama

# Base NVidia CUDA Ubuntu image
FROM $CUDA_FROM

ENV PATH="/usr/local/cuda/bin:${PATH}"

# Install essential packages from ubuntu repository
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends openssh-server openssh-client git git-lfs && \
    apt-get install -y curl && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Install node from upstream, ubuntu packages are too old
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash
RUN apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Install node package manager yarn 
RUN npm install -g yarn


# Install ollama llm inference engine
COPY --from=ollama /usr/bin/ollama /usr/local/ollama/bin/ollama
ENV PATH="/usr/local/ollama/bin:${PATH}"


# Pull a language model (see LICENSE_STABLELM2.txt)
# ARG MODEL=openchat
ARG MODEL=stablelm2:1.6b-zephyr
ENV MODEL=${MODEL}
RUN ollama serve & while ! curl http://localhost:11434; do sleep 1; done; ollama pull $MODEL


# Setup the custom API and frontend
WORKDIR /workspace

# Install backend dependencies
COPY --chmod=755 requirements.txt requirements.txt
RUN pip install -r requirements.txt


# Load sentence-transformers model once in order to cache it in the image
# TODO: ARG / ENV for embedder model
RUN echo "from haystack.components.embedders import SentenceTransformersDocumentEmbedder\nSentenceTransformersDocumentEmbedder(model='svalabs/german-gpl-adapted-covid').warm_up()" | python3


# Install frontend dependencies
COPY --chmod=755 frontend/package.json frontend/package.json
COPY --chmod=755 frontend/yarn.lock frontend/yarn.lock
RUN cd frontend && yarn install


# Copy data
COPY --chmod=755 json_input json_input


# Copy backend for production
COPY --chmod=755 gswikichat gswikichat


# Copy and build frontend for production (into the frontend/dist folder)
COPY --chmod=755 frontend frontend
RUN cd frontend && yarn build


# Container startup script
COPY --chmod=755 start.sh /start.sh
CMD [ "/start.sh" ]
