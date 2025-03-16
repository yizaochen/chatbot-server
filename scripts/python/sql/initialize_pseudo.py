from app.database import SessionLocal
from app.models import (
    User,
    LLMModel,
    Assistant,
)


session = SessionLocal()

try:
    # Create a User
    user = User(email="user@example.com", role="admin", is_active=True)
    session.add(user)
    session.flush()  # Flush to get user.id before commit

    # Create an LLMModel
    llm_model = LLMModel(name="gpt-4o-mini-2024-07-18")
    session.add(llm_model)
    session.flush()  # Flush to get llm_model.id

    # Create an Assistant
    assistant = Assistant(
        user_id=user.id,
        name="AI Assistant",
        system_prompt="You are a helpful assistant.",
        llm_model_id=llm_model.id,
        public=True,
        activated=True,
    )
    session.add(assistant)

    # Commit changes
    session.commit()
    print("User, LLMModel, and Assistant created successfully!")

except Exception as e:
    session.rollback()
    print(f"Error: {e}")
finally:
    session.close()
