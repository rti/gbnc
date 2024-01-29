ARG CUDA_VERSION="11.8.0"
ARG CUDNN_VERSION="8"
ARG UBUNTU_VERSION="22.04"
ARG DOCKER_FROM=nvidia/cuda:$CUDA_VERSION-cudnn$CUDNN_VERSION-devel-ubuntu$UBUNTU_VERSION

# Base NVidia CUDA Ubuntu image
FROM $DOCKER_FROM AS base

# Install essential packages from ubuntu repository
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends openssh-server openssh-client git git-lfs && \
    apt-get install -y curl && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/local/cuda/bin:${PATH}"
ENV HAYSTACK_TELEMETRY_ENABLED="False"
ENV TRUST_REMOTE_CODE="True"

# Install ollama llm inference engine
RUN curl https://ollama.ai/install.sh | sh

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Install fastapi and web server
RUN pip install --upgrade pip
RUN pip install fastapi
RUN pip install "uvicorn[standard]"

# RAG framework haystack
RUN pip install ollama-haystack
RUN pip install farm-haystack[faiss,preprocessing,elasticsearch,inference]
# RUN pip install haystack-ai
# RUN pip install farm-haystack[all]
# RUN pip uninstall -y haystack-ai

# Pull a language model
ARG MODEL=phi
ENV MODEL=${MODEL}
RUN ollama serve & while ! curl http://localhost:11434; do sleep 1; done; ollama pull $MODEL

# Build a language model
# ARG MODEL=discolm
# ENV MODEL=${MODEL}
# WORKDIR /tmp/model
# COPY --chmod=644 Modelfile Modelfile
# RUN curl --location https://huggingface.co/TheBloke/DiscoLM_German_7b_v1-GGUF/resolve/main/discolm_german_7b_v1.Q5_K_S.gguf?download=true --output discolm_german_7b_v1.Q5_K_S.gguf; ollama serve & while ! curl http://localhost:11434; do sleep 1; done; ollama create ${MODEL} -f Modelfile && rm -rf /tmp/model

# Setup the custom API and frontend
WORKDIR /workspace
COPY --chmod=644 gswikichat gswikichat
COPY --chmod=755 frontend frontend
COPY --chmod=755 json_input json_input

# Install node from upstream, ubuntu packages are too old
RUN curl -sL https://deb.nodesource.com/setup_20.x | bash
RUN apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install node package manager yarn 
RUN npm install -g yarn

# Install frontend dependencies and build it for production (into the frontend/dist folder)
RUN cd frontend && yarn install && yarn build

# Container start script
COPY --chmod=755 start.sh /start.sh
CMD [ "/start.sh" ]
