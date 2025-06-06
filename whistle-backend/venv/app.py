from fastapi import FastAPI, HTTPException, Form
import bcrypt

app = FastAPI()

# simulated user DB
user_db = {}

@app.get("/")
async def root():
    return {"message": "whistle backend running. Create Alias # Alias"}

@app.post("/create-alias")
async def create_alias(alias: str = Form(...), password: str = Form(...)):
    if alias in user_db:
        raise HTTPException(status_code=400, detail="Alias already exists. Pick another one")
    
    # hash the password
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode(), salt)
    
    # store user with hashed password
    user_db[alias] = {
        "alias": alias,
        "password_hash": hashed_pw.decode() # to store as str
    }
    
    return {"message": "Alias created successfully"}