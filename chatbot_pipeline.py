
from huggingface_hub import InferenceClient
from agents import Agent
from dotenv import load_dotenv
import os


load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")

if not HF_TOKEN:
    raise RuntimeError("HUGGINGFACE_API_KEY not found in .env")


WEATHER_API_KEY = "51d28cbcfd3ca09c25084491be6497e2"  


agent = Agent(api_key=WEATHER_API_KEY)


client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    token=HF_TOKEN
)

def chat_assistant(prompt):
    
    tool_response = agent.perform_task(prompt)
    if tool_response is not None:
        return str(tool_response)

  
    response = client.chat_completion(
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=512,
        temperature=0.7
    )

    return response.choices[0].message["content"]
