from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    lastName: str
    firstName: str
    department: str
    variant: int
    answers: list[int]
    score: int