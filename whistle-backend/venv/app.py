from fastapi import FastAPI, HTTPException, Form
import bcrypt
import boto3
import os

app = FastAPI()

# user DB
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-west-2',
    endpoint_url='http://localhost:8000'
)
users_table = dynamodb.Table("Users")

@app.get("/")
async def root():
    return {"message": "whistle backend running. Create Alias # Alias"}

@app.post("/create-alias")
async def create_alias(alias: str = Form(...), password: str = Form(...)):
    #check if user exists
    response = users_table.get_item(Key={'alias': alias})
    if 'Item' in response:
        raise HTTPException(status_code=400, detail="Alias already exists. Pick another one")
    
    # hash the password
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode(), salt).decode() # to store as str
    
    # store user with hashed password
    users_table.put_item(
        Item={
           "alias": alias,
        "password_hash": hashed_pw 
        }
    )
        
    
    return {"message": "Alias created successfully"}