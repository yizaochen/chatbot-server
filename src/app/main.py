from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from .routers import users, llm_models, assistants, chat_stream
from app.routers import chat, threads, messages

app = FastAPI()

origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.include_router(users.router)
# app.include_router(llm_models.router)
# app.include_router(assistants.router)
# app.include_router(chat_stream.router)
app.include_router(chat.router)
app.include_router(threads.router)
app.include_router(messages.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


def main():
    import uvicorn

    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)
