import os
import subprocess
import time


import gradio as gr
from openai import OpenAI



client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="token-abc123",
)

"""Need to check how history is getting handled after concurrent use"""

print("Openai Client created")


def predict(message, history):
    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({"role": "assistant", "content": assistant})
    history_openai_format.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=model_name, messages=history_openai_format, temperature=1.0, stream=True
    )

    partial_message = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            partial_message = partial_message + chunk.choices[0].delta.content
            yield partial_message


gr.ChatInterface(predict).queue(default_concurrency_limit=5).launch()
