import requests

# Define the FastAPI server URL
BASE_URL = "http://127.0.0.1:8000"  # Adjust if running on a different port

def test_chat_endpoint():
    url = f"{BASE_URL}/chat"  # Endpoint URL
    payload = {
        "thread_id": 1,
        "input_message": "What is my previous question?"
    }

    response = requests.post(url, json=payload)

    # Assertions
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    
    json_response = response.json()
    assert "message" in json_response, "Response does not contain 'message'"
    assert isinstance(json_response["message"], str), "Message is not a string"

    print("Test Passed! Response:", json_response)

# Run the test
if __name__ == "__main__":
    test_chat_endpoint()
