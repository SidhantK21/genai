from fastapi import FastAPI
from ollama import Client


app=FastAPI()

client = Client(
    host='http://localhost:11434'
)


client.pull('gemma3:1b')

@app.post("/chat")
def chat():
    response=client.chat(model="gemma3:1b",messages=[
        {"role":"user","conten":"Say hi to me"}
    ])
    
    return response['message']['content']