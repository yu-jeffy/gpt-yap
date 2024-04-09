import openai
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

response = client.chat.completions.create(
  model="gpt-4-turbo-preview",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)

content = response.choices[0].message.content
return content