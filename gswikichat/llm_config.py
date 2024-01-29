import os
from haystack_integrations.components.generators.ollama import OllamaGenerator

# TODO: discolm prompt https://huggingface.co/DiscoResearch/DiscoLM_German_7b_v1
print(f"Setting up ollama with {os.getenv('MODEL')}")
llm = OllamaGenerator(
    model=os.getenv("MODEL"),
    url="http://localhost:11434/api/generate"
)
