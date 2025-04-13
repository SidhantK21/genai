import json
import os 
from dotenv import load_dotenv 
from openai import OpenAI
import requests


load_dotenv()

client=OpenAI()

def get_weather (city:str):
    url=f"https://wttr.in/{city}?format=%C+%t"
    response=requests.get(url)

    if response.status_code==200:
        return f"The weather in {city} is {response.text}."
    
    return  "Something went wrong"

def run_command (command):
    result=os.system(command=command)
    return result
    

available_tools={
    "get_weather":{
        "fn":get_weather,
        "description":"Takes city name as input and returns the weather of the city"
    },
    "run_command":{
        "fn":run_command,
        "description":"Takes command as input and execute on the users system and return the result"
    }
}

system_prompt="""  
    You are helpful AI assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.
    For the given user query and avaliable tools plan the step by step execution based on the planning select the relevant tool
    from the available tool. And based on the tool selection you perform an action to call the tool and also give the output to the user in the users language only is english then english if hinglish then hinligh .
    Wait for the observation and based on the observation from the call resolve the user query.
    
    Rules:
    1. Follow the strict JSON output as per schema.
    2. Always perform one step at a time and wait for next input.
    3. Carefully analyse the user query.
    
    Output JSON format:
    {{
        "step":"string"
        "content":"string"
        "function":"The name of function if the step is action"
        "input":"The input parameter of the function"
    }}
    
    Available Tools:
    -get_weather: Takes a city name as input and returns the current weather for the city    
    -run_command:Takes command as user input and runs on the user system 
    
    Examples:
    User Query: What is the weather of New York
    Output:{{"step":"plan","content":"The user is intrested in weather data of New York" }}
    Output:{{"step":"plan","content":"From the available tools i should call get_weather" }}
    Output:{{"step":"action","function":"get_weather","input":"New York" }}
    Output:{{"step":"observe","output":"12 Degree Cel" }}
    Output:{{"step":"output","content":"The weather of New Yokr is 12 Degree Cel" }}
    

    
    

"""

messages=[
    {"role":"system","content":system_prompt}
]
user_query=input("> ")

messages.append({"role":"user","content":user_query})

while True:
    response=client.chat.completions.create(
    model="gpt-4o",
    response_format={"type":"json_object"},
    messages=messages
    )
    
    parsed_ouput=json.loads(response.choices[0].message.content)
    messages.append({"role":"assistant","content":json.dumps(parsed_ouput)})
    
    if parsed_ouput.get("step")=="plan":
        print(f"🧠:{parsed_ouput.get("content")}")
        continue
    
    if parsed_ouput.get("step")=="action":
        tool_name=parsed_ouput.get("function")
        tool_input=parsed_ouput.get("input")
        
        if available_tools.get(tool_name,False)!=False:
            output=available_tools[tool_name].get("fn")(tool_input)
            messages.append({"role":"assistant","content":json.dumps({"step":"observe","output":output})})
            continue
        
    if parsed_ouput.get("step")=="output":
        print(f"🤖:{parsed_ouput.get("content")}")
        break
    
