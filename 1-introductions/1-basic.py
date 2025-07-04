import os
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAPI_KEY"))

completion = client.chat.completions.create(
    model="gpt-4o",
    messages =[
        {
            "role" : "system",
            "content": "You are an helpful assistant",
        },
        {
            "role": "user",
            "content": "Write a joke"
        }
    ]
    
)

response = completion.choices[0].message.content
print(response)