from fastapi import FastAPI, HTTPException, Form, Header
import bcrypt
import boto3
import os
from dotenv import load_dotenv
from jose import JWTError, jwt # type: ignore
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

load_dotenv()

app = FastAPI()

# DynamoDB setup Local--
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    endpoint_url=os.getenv("DYNAMODB_ENDPOINT"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)
users_table = dynamodb.Table("Users")

#JWT config
SECRET_KEY= os.getenv("SECRET_KEY") #TODO:load from AWS Secrets MAnager
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# JWT Utility Functions
def create_access_token(data: dict, expires_delta: timedelta = None): # type: ignore
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # type: ignore

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
        return payload.get("sub")  # return alias
    except JWTError:
        return None


# ----Routes-----

@app.get("/")
async def root():
    return {"message": "whistle backend running. Create Alias # Alias"}

# sign up
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

#sign in
@app.post("/alias")
async def alias(form_data: OAuth2PasswordRequestForm = Depends()):
    alias1 = form_data.alias # type: ignore
    password = form_data.password
    
    # lookup user
    response = users_table.get_item(Key={"alias": alias})
    user = response.get('Item')
    if not user:
        raise HTTPException(status_code=400, detail="Alias not found! Create Aias")
    
    if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        raise HTTPException(status_code=401, detail="Incorrect password")
    # create and return token
    token = create_access_token(data=={"sub":alias}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) # type: ignore
    return {"access_token": token, "token_type": "bearer"}

# protected route
@app.get("/protected")
async def protected_route(authorization: str = Header(...)): # type: ignore
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = authorization.split(" ")[1]
    alias = verify_token(token)
    if not alias:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {"message": f"Hello {alias}, you're authenticated!"}

# logout
@app.post("/logout")
async def logout(authorization: str = Header(...)):
    if not authorization.startswith("Bearer"):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    
    return {"message": "Successfulyy logged out. Please clear the token on client"}

