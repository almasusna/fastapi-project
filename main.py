from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from models import User
import json
from pymongo import MongoClient
import pprint
from bson.objectid import ObjectId


# ------- DB starts here -------
hostname = 'localhost'
port = 27017  

client = MongoClient(hostname, port)
db = client["Quiz-app"]



def findUser(id):
    user = db.Users.find_one({'_id': id})
    return user

def allUsers():
    usersList = []
    users = db.Users.find()
    for user in users:
        usersList.append(user)
    return usersList

def addUser(user):
    db.Users.insert_one(user)

def getQuestions():
    object = db.Questions.find_one({'_id': ObjectId('65b55d5a69b715efc36e7936')})
    return object["questions"]

def getAnswers():
    object = db.Questions.find_one({'_id': ObjectId('65b55d5a69b715efc36e7936')})
    return object["answers"]

questions = getQuestions()
answers = getAnswers()
users = allUsers()
# print(questions)
# print(answers)
# print(users)


# ------ DB ends here ------

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

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Get all questions
@app.get("/questions")
async def get_questions():
    return {"questions": questions}

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
        if (thelist[i] == answers[i]):
            correct += 1
    return {"score": correct}

# Get users with scores
@app.get("/get_users")
async def get_users():
    return {"users": users}


