import os
import json
import requests

from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

client = OpenAI(api_key=(os.getenv("OPENAPI_KEY")))

def search_kb(question : str):
    with open("kb.json", "r") as f:
        return json.load(f)

tools = [{
    "type": "function",
    "name": "search_kb",
    "description": "Get the answer to the user's question from the knowledge base.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string"},
        },
        "required": ["question"],
        "additionalProperties": False
    },
    "strict": True
}]

input_messages = [{"role": "user", "content": "What is the return policy?"}]

response = client.responses.create(
    model="gpt-4o",
    input=input_messages,
    tools=tools,
)

tool_call = response.output[0]
args = json.loads(tool_call.arguments)

result = search_kb(args["question"])

input_messages.append(tool_call)
input_messages.append({
    "type": "function_call_output",
    "call_id": tool_call.call_id,
    "output": str(result)
})

response_2 = client.responses.create(
    model="gpt-4o",
    input=input_messages,
    tools=tools,
)
# print(response_2.output_text)

class KBResponse(BaseModel):
    answer: str = Field(description="The answer to user's question.")
    source: int = Field(description="The record id of the answer.")

response_3 = client.responses.parse(
    model="gpt-4o",
    input=input_messages,
    tools=tools,
    text_format=KBResponse
)
print(response_3.output_parsed)