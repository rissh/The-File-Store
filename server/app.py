from fastapi import FastAPI, UploadFile, HTTPException, Query, File
from fastapi.responses import JSONResponse
from pathlib import Path
import os, re
from typing import List 
from collections import Counter

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

@app.get("/wc")
def word_count():
    """
    Count the total number of words in all files stored in the server.
    """
    total_words = 0
    for file_name in os.listdir(STORAGE_DIR):
        if file_name.startswith("."):  # Ignore hidden files
            continue

        file_path = os.path.join(STORAGE_DIR, file_name)
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                content = f.read()
                total_words += len(re.findall(r'\w+', content))  # Counting words

    return {"total_word_count": total_words}

@app.get("/freq-words")
def freq_words(limit: int = Query(10, alias="n"), order: str = Query("dsc")):
    """
    Get the most or least frequent words across all files.
    """
    word_counts = Counter()

    # Read and process each file in the storage directory
    for file_name in os.listdir(STORAGE_DIR):
        file_path = os.path.join(STORAGE_DIR, file_name)
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                content = f.read()
                # Tokenize words and update the counter
                words = re.findall(r'\w+', content.lower())  # Case insensitive
                word_counts.update(words)

    # Sort by frequency
    sorted_words = word_counts.most_common() if order == "dsc" else sorted(word_counts.items(), key=lambda x: x[1])

    # Limit the results
    result = sorted_words[:limit]

    return {"words": result}