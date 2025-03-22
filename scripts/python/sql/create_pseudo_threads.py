from app.database import SessionLocal
from app.models import Thread, Message


session = SessionLocal()
user_id = 1
assistant_id = 1
names = ["Thread 2", "Thread 3", "Thread 4"]
messages = [
    ("human", "Hello!"),
    ("ai", "Hello! How can I help you today?"),
    ("human", "I need help with my account."),
    ("ai", "Sure! What is your account number?"),
    ("human", "123456"),
    ("ai", "Thank you!"),
    ("human", "You're welcome!"),
    ("ai", "Goodbye!"),
]


try:
    for thread_name in names:
        new_thread = Thread(
            user_id=user_id,
            assistant_id=assistant_id,
            name=thread_name,
        )
        session.add(new_thread)
        session.commit()
        for message in messages:
            new_message = Message(
                thread_id=new_thread.id,
                ai_generated=message[0] == "ai",
                content=message[1],
            )
            session.add(new_message)
            session.commit()
        print(f"Thread '{thread_name}' created successfully!")


except Exception as e:
    session.rollback()
    print(f"Error: {e}")
finally:
    session.close()
