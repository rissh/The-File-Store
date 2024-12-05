from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
from typing import List 

app = FastAPI()

STORAGE_DIR = "./storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Welcome to the File Store!"}

@app.post("/upload")
async def add_file(files: List[UploadFile]):
    """
    Upload files to the server.
    """
    responses = []

    for file in files:
        file_path = os.path.join(STORAGE_DIR, file.filename)

        if os.path.exists(file_path):
            raise HTTPException(status_code=400, detail=f"File '{file.filename}' already exists.")

        with open(file_path, "wb") as f:
            f.write(await file.read())

        responses.append({"file": file.filename, "message": "File uploaded successfully"})

    return responses

@app.get("/list")
def list_files():
    files = []
    for file_name in os.listdir(STORAGE_DIR):

        if file_name.startswith("."):   #Hidden files
            continue

        file_path = os.path.join(STORAGE_DIR, file_name)
        if os.path.isfile(file_path):
            files.append({"name": file_name, "size": os.path.getsize(file_path)})
    
    if not files:
        return {"message": "No files found."}
    
    return {"files": files}
