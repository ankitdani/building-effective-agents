import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

client = OpenAI(api_key=(os.getenv("OPENAPI_KEY")))

completion = client.chat.completions.parse(
    model = "gpt-4o",
    messages=[
        {
            "role" : "system",
            "content": "Extract the event information.",
        },
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday."
        },
    ],
    response_format=CalendarEvent
)

event = completion.choices[0].message.parsed
print(event)



# import os
# from openai import OpenAI
# from dotenv import load_dotenv
# from pydantic import BaseModel

# load_dotenv()

# class CalendarEvent(BaseModel):
#     name: str
#     date: str
#     participants: list[str]

# client = OpenAI(api_key=(os.getenv("OPENAPI_KEY")))

# completion = client.responses.parse(
#     model = "gpt-4o",
#     input=[
#         {
#             "role" : "system",
#             "content": "Extract the event information.",
#         },
#         {
#             "role": "user",
#             "content": "Alice and Bob are going to a science fair on Friday."
#         },
#     ],
#     text_format=CalendarEvent
# )

# event = completion.output_parsed
# print(event)
