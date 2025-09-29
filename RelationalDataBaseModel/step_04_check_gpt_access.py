## This python program would connect to GPT and check if the connection is successful.
import openai
import os
from openai import OpenAI

# Load your API key from an environment variable or secret management service
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")  

# initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Test the connection by making a simple request
response = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "what is the value of 4 + 3?"},
    ]
)

#print only the relevant part of the response
print("Model answer is:", response.choices[0].message.content)