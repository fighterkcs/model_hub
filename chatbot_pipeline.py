# from huggingface_hub import InferenceClient
# from transformers import pipeline
# import textwrap
# from agents import Agent

# import os
# from dotenv import load_dotenv
# load_dotenv()
# HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")
# agent = Agent(api_key=os.getenv("API_KEY"))
# if not HF_TOKEN:
#     raise RuntimeError(
#         "HUGGINGFACE_API_KEY not found. "
#         "Check your .env file or environment variables."
#     )

# model_1 = "mistralai/Mistral-7B-Instruct-v0.3"
# model_2 = "HuggingFaceH4/zephyr-7b-beta"

# client1 = InferenceClient(
#     model=model_1,
#     token=HF_TOKEN
# )

# client2 = InferenceClient(
#     model=model_2,
#     token=HF_TOKEN
# )

# summarizer = pipeline(
#     "summarization",
#     model="facebook/bart-large-cnn"
# )

# def chat_assistant(input1):
#     tool_response = agent.perform_task(input1)
#     if tool_response:
#         return tool_response
    
    
#     messages = [
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": input1}
#     ]

#     try:
#         # PRIMARY MODEL
#         response = client1.chat_completion(
#             messages=messages,
#             max_tokens=512,
#             temperature=0.7
#         )
#     except Exception:
#         # FALLBACK MODEL
#         response = client2.chat_completion(
#             messages=messages,
#             max_tokens=512,
#             temperature=0.7
#         )

#     answer = response.choices[0].message["content"].strip()
#     answer = textwrap.fill(answer, width=80)

#     summary = summarizer(
#         answer,
#         max_length=150,
#         min_length=40,
#         do_sample=False
#     )

#     return summary[0]["summary_text"]

# chatbot_pipeline.py

from huggingface_hub import InferenceClient
from agents import Agent
from dotenv import load_dotenv
import os

# -------------------------------
# Load only Hugging Face token
# -------------------------------
load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")

if not HF_TOKEN:
    raise RuntimeError("HUGGINGFACE_API_KEY not found in .env")

# -------------------------------
# HARD-CODE WEATHER API KEY HERE
# -------------------------------
WEATHER_API_KEY = "51d28cbcfd3ca09c25084491be6497e2"  

# Initialize agent with weather key
agent = Agent(api_key=WEATHER_API_KEY)

# LLM client
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    token=HF_TOKEN
)

def chat_assistant(prompt):
    # 1️⃣ Try Calculator / Weather first
    tool_response = agent.perform_task(prompt)
    if tool_response is not None:
        return str(tool_response)

    # 2️⃣ Fallback to LLM
    response = client.chat_completion(
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=512,
        temperature=0.7
    )

    return response.choices[0].message["content"]
