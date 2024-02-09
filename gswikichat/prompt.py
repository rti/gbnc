from haystack.components.builders.prompt_builder import PromptBuilder

prompt_template_en = """
<|system|>
You are a helpful assistant. You answer questions based on the given documents.
Answer based on the documents only. If the information is not in the documents,
say that you cannot find the information.
<|endoftext|>
<|user|>
Documents:
{% for doc_ in documents %}
    {{ doc_.content }}
{% endfor %}
With this documents, answer the following question: {{question}}
<|endoftext|>
<|assistant|>
"""

prompt_template_de = """
<|system|>
Du bist ein hilfreicher Assistent. Du beantwortest Fragen basierend auf den vorliegenden Dokumenten.
Beantworte basierend auf den Dokumenten nur. Wenn die Information nicht in den Dokumenten ist,
sage, dass du sie nicht finden kannst.
<|endoftext|>
<|user|>
Dokumente:
{% for doc_ in documents %}
    {{ doc_.content }}
{% endfor %}
Mit diesen Dokumenten, beantworte die folgende Frage: {{question}}
<|endoftext|>
<|assistant|>
"""

prompt_builders = {
    'en': PromptBuilder(template=prompt_template_en),
    'de': PromptBuilder(template=prompt_template_de),
}
