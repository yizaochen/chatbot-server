from fastapi import FastAPI
from .routers import users, llm_models, assistants, chat

app = FastAPI()

app.include_router(users.router)
app.include_router(llm_models.router)
app.include_router(assistants.router)
app.include_router(chat.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


def main():
    import uvicorn

    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)
