import requests

BASE_URL = "http://127.0.0.1:8000/threads"  # Adjust if your FastAPI server runs elsewhere


def test_get_threads(user_id):
    """Manually tests the get_threads endpoint."""
    url = f"{BASE_URL}/{user_id}"
    response = requests.get(url)

    print(f"Testing GET {url}")
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        print("Response JSON:", data)
    except requests.exceptions.JSONDecodeError:
        print("Response is not valid JSON:", response.text)


if __name__ == "__main__":
    # Test with a valid user ID
    test_get_threads(1)
