import json
from dotenv import load_dotenv
import os
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

system_prompt = """
You are an AI assistant who is expert in breaking down complex problems and resolving them step-by-step.

For a given user input, analyze it and break it down into at least 5-6 logical steps before solving it.

Return each step in a strict JSON format, one step per line, with fields: "step" and "content".

Example:
Input: What is 2+2 
{"step": "analyze", "content": "The user is asking a basic arithmetic question."}
{"step": "think", "content": "To answer this, I need to perform addition on the numbers 2 and 2."}
{"step": "calculate", "content": "2 + 2 equals 4."}
{"step": "validate", "content": "The result 4 is correct for the expression 2 + 2."}
{"step": "result", "content": "The final answer is 2 + 2 = 4, obtained by adding the two numbers together."}
"""

messages = [{"role": "system", "content": system_prompt}]

query = input("User query: ")
messages.append({"role": "user", "content": query})

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=1,
    messages=messages
)

# Split multi-line JSON objects and parse them one by one
response_lines = response.choices[0].message["content"].strip().split("\n")

for line in response_lines:
    try:
        parsed = json.loads(line)
        if parsed["step"] != "result":
            print(f"🧠 [{parsed['step']}] {parsed['content']}")
        else:
            print(f"🤖 [{parsed['step']}] {parsed['content']}")
            break
    except json.JSONDecodeError:
        print("⚠️ Could not parse line as JSON:", line)
