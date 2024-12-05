from fastapi import FastAPI, UploadFile, HTTPException, Query, File
from fastapi.responses import JSONResponse
from pathlib import Path
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

@app.delete("/delete")
async def delete_file(filename: str = Query(...)):
    """
    Delete a file from the server.
    """
    file_path = Path(STORAGE_DIR) / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found")

    try:
        file_path.unlink()  # Delete the file
        return {"message": f"File '{filename}' deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")
    
@app.put("/update")
async def update_file(filename: str, file: UploadFile = File(...)):
    """
    Update the contents of an existing file, or create it if it doesn't exist.
    """
    file_path = Path(STORAGE_DIR) / filename

    # If the file already exists, it will be overwritten
    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"message": f"File '{filename}' updated/created successfully!"}
