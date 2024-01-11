from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from models import User
import json

app = FastAPI()

origins = [
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = []
questions = {}

with open("data.json", encoding = 'utf-8', mode = 'r') as my_file:
    data = my_file.read()
    questions = json.loads(data)

with open("data.json", encoding = 'utf-8', mode = 'r') as my_file:
    data = my_file.read()
    questions = json.loads(data)



@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Get all questions
@app.get("/questions")
async def get_questions():
    return {"questions": questions["questions"]}

# Create a user
@app.post("/add_user")
async def add_user(user: User):
    theUser = user
    theUser.score = checkAnswers(user.answers)
    users.append(theUser)
    return {"score": theUser.score}

def checkAnswers(thelist):
    correct = 0
    for i in range(len(thelist)):
        if (thelist[i] == questions["answers"][i]):
            correct += 1
    return {"score": correct}

# Get users with scores
@app.get("/get_users")
async def get_users():
    return {"users": users}


