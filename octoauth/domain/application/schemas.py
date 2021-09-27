from pydantic import BaseModel


class ApplicationReadDTO(BaseModel):
    uid: str
    name: str
    description: str


class ApplicationWriteDTO(BaseModel):
    name: str
    description: str
