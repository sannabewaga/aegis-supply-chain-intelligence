import os
from google import genai

api_key = dbutils.secrets.get(
    scope="aegis-secrets",
    key="gemini-api-key"
)

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Say hello to Aegis in one sentence."
)

print(response.text)