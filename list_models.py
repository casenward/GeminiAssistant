from google import genai
import os

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"], http_options={"api_version": "v1"})

for m in client.models.list():
    print(m.name)
