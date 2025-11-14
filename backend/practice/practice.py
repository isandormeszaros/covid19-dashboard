from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

user_db = {
    'jack': {'username': 'jack', 'date_joined': '2021-12-01', 'location': 'New York', 'age': 28},
    'jill': {'username': 'jill', 'date_joined': '2021-12-02', 'location': 'Los Angeles', 'age': 19},
    'jane': {'username': 'jane', 'date_joined': '2021-12-03', 'location': 'Toronto', 'age': 52}
}

app = FastAPI()

class User(BaseModel):
    username : str
    date_joined : str
    location : str
    age : int

class UserOptional(BaseModel):
    username: Optional[str] = None
    date_joined: Optional[str] = None
    location: Optional[str] = None
    age: Optional[int] = None

@app.get("/")
def my_first_api():
    return {"Output" : "this is my first FastAPI"}

@app.get("/users")
def get_users():    
    user_list = list(user_db.values())
    return user_list

@app.get("/users/limit")
def get_user_limit(limit: int):
# def get_user_limit(limit: 2): default value
    user_list = list(user_db.values())
    return user_list[:limit]

@app.get("/users/{user}")
def get_user_name(user: str):
    return user_db[user]

@app.post("/users")
def post_username(user: User):
    username = user.username 
    user_db[username] = user.dict()
    return user

@app.delete("/users/{user}")
def delete_users(username: str):
    del user_db[username]
    user_list = list(user_db.values())
    return user_list

# PUT - all data 
@app.put("/users/{username}")
def put_users(username: str, user : User):
    user_db[username] = user.dict()
    return list(user_db.values())

# PATCH - partial update
@app.patch("/users/{username}")
def update_user(username: str, patch: UserOptional):
    if username not in user_db:
        return {"Err": "No user"}

    stored_user = user_db[username]
    patch_data = patch.model_dump(exclude_none=True)
    
    stored_user.update(patch_data)
    return list(user_db.values())