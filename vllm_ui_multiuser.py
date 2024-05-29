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
print("Launching the server")
command = f"python -m vllm.entrypoints.openai.api_server --model {model_name} --dtype {dtype} --api-key {api_key} --trust-remote-code"

# Use shell=True only if the command is simple and doesn't contain special characters
# process = subprocess.Popen(
#     command, shell=True, stdout=open("my_logfile.log", "a"), stderr=subprocess.PIPE
# )
os.system(command)
