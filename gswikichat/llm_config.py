import os
from haystack_integrations.components.generators.ollama import OllamaGenerator

import logging
logger = logging.getLogger()

OLLAMA_MODEL_NAME = os.environ.get("OLLAMA_MODEL_NAME")
OLLAMA_URL = os.environ.get("OLLAMA_URL")
OLLAMA_GENERATE_URL = f"{OLLAMA_URL}/api/generate"

logger.info(f'Using {OLLAMA_MODEL_NAME=}')
logger.info(f'Endpoint: {OLLAMA_URL=}')
logger.info(f'Generate: {OLLAMA_GENERATE_URL=}')

logger.debug(f'I AM HERE')

print(f"Setting up ollama with {OLLAMA_MODEL_NAME}")
llm = OllamaGenerator(
    model=OLLAMA_MODEL_NAME,
    url=OLLAMA_GENERATE_URL
)
