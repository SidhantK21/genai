from dotenv import load_dotenv
import os
import openai

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=api_key)

system_prompt="""
Your are an ai assistant who is expert in breaking down complex problems and then resoolve it 

For the given user input,analyse  the input and break down  the problem step by step.
Atleast 5-6 steps how to solve the problem before solving it down .

The steps are you get a user input you analyse you think you again think for several times and then you return the output with explanation validate also before sending the output  

Follow the strict json output as per the output schema and always perform one step at a time carefully before proceeding to the next step

Example:
Input:What is 2+2 
Output:{{"step":"analyse","content":"Alright the user is interested in maths" }}
Output:{{"step":"think","content":"To perform this action i must add these numbers" }}
Output:{{"step":"output","content":"4" }}
Output:{{"step":"validate","content":"seems like 4 is correct and for 2+2 " }}
Output:{{"step":"result","content":"2+2=4 and that is calculated by adding all numbers " }}




"""

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=2,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "4+4"},
    ]
)

print(response.choices[0].message.content)
