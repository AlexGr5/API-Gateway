import requests
import json  # Для работы с JSON

url = "http://localhost:8000/send"
data = {"message": "Hello from HTTP client!"}

response = requests.post(url, json=data)
print("Client ask API and get answer.")
print("Message send: " + json.dumps(data))
print("Message receive: " + response.json())
