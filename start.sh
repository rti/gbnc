#!/bin/bash

if [[ $PUBLIC_KEY ]]
then
    mkdir -p ~/.ssh
    chmod 700 ~/.ssh
    cd ~/.ssh
    echo $PUBLIC_KEY >> authorized_keys
    chmod 700 -R ~/.ssh
    cd /
    service ssh start
else
    echo "No public key provided, skipping ssh setup"
fi

echo "Starting ollama"
ollama serve &

cd /workspace

echo "Starting api"
uvicorn api:app --host 0.0.0.0 --port 8000 &

echo "Sleeping..."
sleep infinity