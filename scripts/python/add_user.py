import requests

# Define the FastAPI server URL
BASE_URL = "http://localhost:8000/api/users/"

# Define the user payload
user_data = {"email": "user@example.com", "role": "admin", "is_active": True}

# Send the POST request
response = requests.post(BASE_URL, json=user_data)

# Print the response
if response.status_code == 200:
    print("User created successfully:", response.json())
else:
    print("Failed to create user:", response.status_code, response.text)
