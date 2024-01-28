from haystack.components.builders.prompt_builder import PromptBuilder

prompt_template = """
Given these documents, answer the question. Answer in a full sentence. Give the response only, no explanation. Don't mention the documents.
Documents:
{% for doc in documents %}
    If {{ doc.content }} answers the Question: {{question}}
    Then return {{ doc.meta["src"] }}
{% endfor %}
"""

# prompt_template = """
# Given these documents, answer the question. Answer in a full sentence. Give the response only, no explanation. Don't mention the documents.
# Documents:
# If {{ doc.content }} answers the Question: {{question}}
# Then only return {{ doc.meta["src"] }} and nothing at all.
# {% endfor %}
# """

prompt_builder = PromptBuilder(template=prompt_template)
