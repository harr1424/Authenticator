import hashlib
import hmac
import os
from typing import Tuple
import boto3
import uvicorn
from fastapi import FastAPI, Form

app = FastAPI()
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('clients')

@app.get("/")
async def root():
    info = table.creation_date_time
    return {"Hello World!"}


def hash_new_password(password: str) -> Tuple[bytes, bytes]:
    """
    Hash the provided password with a randomly-generated salt,
    encode as base64, and return the salt and hash for storage.
    """
    salt = os.urandom(64)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt, hashed_password


def is_correct_password(salt: bytes, hashed_password: bytes, password: str) -> bool:
    """
    Given a previously-stored salt/hash and a password in a current
    authentication attempt check whether the password is correct.
    """
    return hmac.compare_digest(
        hashed_password,
        hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    )

@app.post("/register/")
async def register(username: str = Form(...), password: str = Form(...)):
    """
    Accepts an email address and password as parameters, calls hash_new_password in order
    to hash and salt the password and then stores the email, salt, and hashed password in a
    DynamoDB table.
    :param username:
    :param password:
    :return:
    """
    salt, hashed_password = hash_new_password(password)
    table.put_item(
        Item= {
            'email': username,
            'salt': salt,
            'password': hashed_password
        }
    )
    return {f"Success! {username} has been registered."}


@app.post("/authenticate/")
async def authenticate(username: str = Form(...), password: str = Form(...)):
    """
    Accepts a previously registered email and password combination, if valid this function
    will return redirect to API root after setting a session cookie.
    :param username:
    :param password:
    :return:
    """
    try:
        response = table.get_item(Key={'email': username})
        item = response['Item']
        stored_salt = item['salt'].value
        stored_password = item['password'].value
        return is_correct_password(stored_salt, stored_password, password)
    except KeyError:
        return "The email you entered has not been registered."


@app.post("/authenticate_no_form/")
async def authenticate_no_form(username: str, password: str):
    """
    Accepts a previously registered email and password combination, if valid this function
    will return redirect to API root after setting a session cookie.
    :param username:
    :param password:
    :return:
    """
    try:
        response = table.get_item(Key={'email': username})
        item = response['Item']
        stored_salt = item['salt'].value
        stored_password = item['password'].value
        return is_correct_password(stored_salt, stored_password, password)
    except KeyError:
        return "The email you entered has not been registered."

if __name__ == '__main__':
    uvicorn.run("main:app", host='localhost', port=5555, reload=True)
