import os
import subprocess
import time

os.system("pip install vllm -Uqq")
os.system("pip install gradio -Uqq")

import gradio as gr
from openai import OpenAI

import argparse

parser = argparse.ArgumentParser(description='Start the vllm server with openai endpoint')

parser.add_argument('--model_name', type=str, default='microsoft/Phi-3-mini-4k-instruct',
                    help='Name of the model to host')
parser.add_argument('--api_key', type=str, default='token-abc123',
                    help='API key for client auth')
parser.add_argument('--dtype', type=str, default='float16',
                    help='Data type for model parameters')

args = parser.parse_args()

model_name = args.model_name
api_key = args.api_key
dtype = args.dtype

model_name = "microsoft/Phi-3-mini-4k-instruct"

api_key = "token-abc123"

command = f"nohup python -m vllm.entrypoints.openai.api_server --model {model_name} --dtype {dtype} --api-key {api_key} --trust-remote-code &"

# Use shell=True only if the command is simple and doesn't contain special characters
process = subprocess.Popen(
    command, shell=True, stdout=open("my_logfile.log", "a"), stderr=subprocess.PIPE
)

pid = process.pid
# print(f"Process started with PID: {pid}")


print("Waiting for the server to start..\r", end="")
time.sleep(120)
print("")


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
