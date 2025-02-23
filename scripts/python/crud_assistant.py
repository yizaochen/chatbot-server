import requests

BASE_URL = "http://localhost:8000/api/assistant"


def create_assistant(
    user_id: int,
    name: str,
    system_prompt: str,
    llm_model_id: int,
    public: bool,
    activated: bool,
):
    payload = {
        "user_id": user_id,
        "name": name,
        "system_prompt": system_prompt,
        "llm_model_id": llm_model_id,
        "public": public,
        "activated": activated,
    }
    response = requests.post(BASE_URL, json=payload)
    return response.json()


def get_all_assistants():
    response = requests.get(BASE_URL)
    return response.json()


def get_assistant(assistant_id: int):
    response = requests.get(f"{BASE_URL}/{assistant_id}")
    return response.json()


def update_assistant(
    assistant_id: int,
    name: str = None,
    system_prompt: str = None,
    llm_model_id: int = None,
    public: bool = None,
    activated: bool = None,
):
    payload = {
        "name": name,
        "system_prompt": system_prompt,
        "llm_model_id": llm_model_id,
        "public": public,
        "activated": activated,
    }
    payload = {k: v for k, v in payload.items() if v is not None}  # Remove None values
    response = requests.put(f"{BASE_URL}/{assistant_id}", json=payload)
    return response.json()


def delete_assistant(assistant_id: int):
    response = requests.delete(f"{BASE_URL}/{assistant_id}")
    return response.json()


def main():
    while True:
        print("\nChoose an operation:")
        print("1. Create Assistant")
        print("2. Get All Assistants")
        print("3. Get Single Assistant")
        print("4. Update Assistant")
        print("5. Delete Assistant")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user_id = int(input("Enter user ID: "))
            name = input("Enter assistant name: ")
            system_prompt = input("Enter system prompt: ")
            llm_model_id = int(input("Enter LLM model ID: "))
            public = input("Is it public? (true/false): ").lower() == "true"
            activated = input("Is it activated? (true/false): ").lower() == "true"
            print(
                create_assistant(
                    user_id, name, system_prompt, llm_model_id, public, activated
                )
            )

        elif choice == "2":
            print(get_all_assistants())

        elif choice == "3":
            assistant_id = int(input("Enter assistant ID: "))
            print(get_assistant(assistant_id))

        elif choice == "4":
            assistant_id = int(input("Enter assistant ID: "))
            name = input("Enter new name (leave blank to keep unchanged): ")
            system_prompt = input(
                "Enter new system prompt (leave blank to keep unchanged): "
            )
            llm_model_id = input(
                "Enter new LLM model ID (leave blank to keep unchanged): "
            )
            public = input("Is it public? (true/false/leave blank to keep unchanged): ")
            activated = input(
                "Is it activated? (true/false/leave blank to keep unchanged): "
            )

            name = name if name else None
            system_prompt = system_prompt if system_prompt else None
            llm_model_id = int(llm_model_id) if llm_model_id else None
            public = public.lower() == "true" if public else None
            activated = activated.lower() == "true" if activated else None

            print(
                update_assistant(
                    assistant_id, name, system_prompt, llm_model_id, public, activated
                )
            )

        elif choice == "5":
            assistant_id = int(input("Enter assistant ID: "))
            print(delete_assistant(assistant_id))

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
