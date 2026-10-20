import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from functions import available_functions, call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("No Openrouter API Key found")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def get_response(query: str, history: list[dict[str, str]] | None = None, temperature: float = 0.5):
    if history is None:
        history = []
    history.append({
        "role": "user",
        "content": query,
    })
    return client.chat.completions.create(
        model="openrouter/free",
        messages=history,
        temperature=temperature,
        tools=available_functions,
    )

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

query = args.user_prompt

messages = [
    {"role": "system", "content": system_prompt}
]

for _ in range(20):
    response = get_response(query, messages, 0.6)
    message = response.choices[0].message
    usage = response.usage
    if args.verbose:
        print("User prompt: ", query)
        print("Prompt tokens:", usage.prompt_tokens)
        print("Response tokens:", usage.completion_tokens)

    messages.append(message)
    print("Response:", message.content, sep="\n")
    if message.tool_calls is None or len(message.tool_calls) == 0:
        break
    for tool_call in message.tool_calls:
        result_message = call_function(tool_call, args.verbose)
        if args.verbose:
            print(f"-> {result_message['content']}")
        messages.append(result_message)
