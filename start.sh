#!/bin/bash

set -e
set -x

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


echo "Setting up postgres database server with vecto.rs extension"

service postgresql start

su postgres <<'EOF'
psql -c 'ALTER SYSTEM SET shared_preload_libraries = "vectors.so"'
psql -c 'ALTER SYSTEM SET search_path TO "$user", public, vectors'
EOF

service postgresql restart

cat > ~/.env <<EOF
DB_USER=postgres
DB_PASS=$(openssl rand -base64 32)
DB_NAME=gbnc
export DB_USER
export DB_PASS
export DB_NAME
EOF

source ~/.env

echo "source ~/.env" >> ~/.bashrc

su --preserve-environment postgres <<'EOF'
psql -c "CREATE EXTENSION vectors;"
psql -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASS';"
psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
EOF


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
