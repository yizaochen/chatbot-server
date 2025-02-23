import requests

url = "http://localhost:8000/api/llm_model/"
data = {"name": "gpt-4o"}

response = requests.post(url, json=data)
print(response.json())
