#!/bin/bash

set -e

if [[ $PUBLIC_KEY ]]
then
    mkdir -p ~/.ssh
    chmod 700 ~/.ssh
    cd ~/.ssh
    echo "$PUBLIC_KEY" >> authorized_keys
    chmod 700 -R ~/.ssh
    cd /
    service ssh start
else
    echo "No public key provided, skipping ssh setup"
fi

echo "Starting ollama"
ollama serve &

while ! curl "$OLLAMA_URL"; do 
    sleep 1 
done

echo "Pulling $OLLAMA_MODEL_NAME from ollama library"
ollama pull "$OLLAMA_MODEL_NAME"

cd /workspace

echo "Starting api"
uvicorn gswikichat:app --reload --host 0.0.0.0 --port 8000 &

echo "Ready"
sleep infinity
