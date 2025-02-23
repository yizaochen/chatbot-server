from pydantic import BaseModel


class LLMModelCreate(BaseModel):
    name: str


class LLMModelRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
