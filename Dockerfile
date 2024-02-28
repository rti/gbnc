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

# Install unattendedly
ENV DEBIAN_FRONTEND=noninteractive

# Force a config for tzdata package, otherwise it will interactively ask during install
RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime

# Install essential packages from ubuntu repository
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends openssh-server openssh-client git git-lfs && \
    apt-get install -y curl && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get install -y postgresql-14 && \
    apt-get install -y jq && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Install vecto.rs extension to postgres
RUN curl -L -O https://github.com/tensorchord/pgvecto.rs/releases/download/v0.2.0/vectors-pg14_0.2.0_amd64.deb
RUN dpkg -i vectors-pg14_0.2.0_amd64.deb


# Install node from upstream, ubuntu packages are too old
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Install node package manager yarn 
RUN npm install -g yarn


# Install ollama llm inference engine
COPY --from=ollama /usr/bin/ollama /usr/local/ollama/bin/ollama
ENV PATH="/usr/local/ollama/bin:${PATH}"


# Setup the app in workspace
WORKDIR /workspace

# Install backend dependencies
COPY --chmod=755 requirements.txt requirements.txt
RUN pip install -r requirements.txt


# Pull a language model (see LICENSE_STABLELM2.txt)
# ARG OLLAMA_MODEL_NAME=openchat
ARG OLLAMA_MODEL_NAME=stablelm2:1.6b-zephyr
ARG OLLAMA_URL=http://localhost:11434

ENV OLLAMA_MODEL_NAME=${OLLAMA_MODEL_NAME}
ENV OLLAMA_URL=${OLLAMA_URL}

# TODO: cache path
RUN ollama serve & while ! curl ${OLLAMA_URL}; do sleep 1; done; ollama pull $OLLAMA_MODEL_NAME


# Load sentence-transformers model once in order to cache it in the image
# TODO: ARG / ENV for embedder model
# TODO: SENTENCE_TRANSFORMERS_HOME for cache path
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
