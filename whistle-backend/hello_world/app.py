from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from typing import List, Optional
import uuidi
import boto3
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Whistle backend running"}

@app.post("/leaks")
async def drop_leak(
    text: str = Form(...),
    hashtags: Optional[str] = Form(""),
    image: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None)
):
    leak_id = str(uuid.uuid4())
    # TODO: upload media to s3 and save metadata to DynamoDB
    
    return JSONResponse({
        "leak_id": leak_id,
        "status": "saved(mock)",
    })
