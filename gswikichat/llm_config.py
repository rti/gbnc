import os
from haystack_integrations.components.generators.ollama import OllamaGenerator

# import logging
# logger = logging.getLogger()

print(f"Setting up ollama with {os.getenv('MODEL')}")
llm = OllamaGenerator(
    model=os.getenv("MODEL"),
    url="http://localhost:11434/api/generate"
)
