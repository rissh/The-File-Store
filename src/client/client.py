import typer
import requests
from pathlib import Path
from typing import List

app = typer.Typer()

BASE_URL = "http://127.0.0.1:8000"

@app.command()
def hello():
    """
    Say hello to the server.
    """
    typer.echo("Hello! The File Store client is ready to use.")


@app.command()
def add(files: List[Path]):
    """
    Add files to the store.
    """
    file_data = []
    failed_files = []  # already exist

    for file in files:
        if not file.exists():
            typer.echo(f"File '{file}' does not exist locally.")
            raise typer.Exit(code=1)  # File does not exist locally
        
        # if the file already exists
        response = requests.get(f"{BASE_URL}/list")
        existing_files = [file['name'] for file in response.json().get('files', [])]

        if file.name in existing_files:
            failed_files.append(file.name)
            typer.echo(f"Error: File '{file.name}' already exists.")
            continue  # Skip and continue with others

        # If the file doesn't exist
        file_data.append(("files", (file.name, file.open("rb"))))

    # Send files
    if file_data:
        response = requests.post(f"{BASE_URL}/upload", files=file_data)

        if response.status_code == 200:
            typer.echo("Files uploaded successfully!")
            # Details for uploaded file
            for file_response in response.json():
                typer.echo(f"File: {file_response['file']} - {file_response['message']}")
        else:
            typer.echo(f"Unexpected error: {response.text}")
            raise typer.Exit(code=1)

    # skipped files
    if failed_files:
        typer.echo(f"\nThe following files were not uploaded because they already exist on the server:")
        for failed_file in failed_files:
            typer.echo(f"- {failed_file}")

    
@app.command()
def ls():
    """
    List all files stored on the server.
    """
    response = requests.get(f"{BASE_URL}/list")

    if response.status_code == 200:
        data = response.json()
        if "files" in data:
            typer.echo("Files on the server:")
            for file in data["files"]:
                typer.echo(f"- {file['name']} ({file['size']} bytes)")
        else:
            typer.echo(data["message"])  # No files found
    else:
        typer.echo("Failed to fetch file list from the server.")

@app.command()
def rm(filename: str):
    """
    Remove a file from the store.
    """
    typer.echo(f"Attempting to remove file: {filename}")

    # DELETE request
    response = requests.delete(f"{BASE_URL}/delete", params={"filename": filename})

    if response.status_code == 200:
        typer.echo(f"File '{filename}' removed successfully!")
    elif response.status_code == 404:
        typer.echo(f"File '{filename}' not found on the server.")
    else:
        typer.echo(f"Error: {response.text}")

@app.command()
def update(filename: str, file: Path):
    """
    Update the content of a file on the server, or create it if it does not exist.
    """
    if not file.exists():
        typer.echo(f"Local file '{file}' does not exist.")
        raise typer.Exit(code=1)  # Exit if local file not exist

    with file.open("rb") as f:
        file_data = f.read()  

    # Sending request
    response = requests.put(f"{BASE_URL}/update?filename={filename}", files={"file": (filename, file_data)})

    if response.status_code == 200:
        typer.echo(f"File '{filename}' updated/created successfully!")
    else:
        typer.echo(f"Error: {response.text}")
        raise typer.Exit(code=1)  # Exit 
    
@app.command()
def wc():
    """
    Get the total word count from all files stored on the server.
    """
    response = requests.get(f"{BASE_URL}/wc")

    if response.status_code == 200:
        word_count = response.json()
        typer.echo(f"Total word count across all files: {word_count['total_word_count']}")
    else:
        typer.echo(f"Error: {response.text}")
        raise typer.Exit(code=1)
    
@app.command()
def freq_words(n: int = 10, order: str = "dsc"):
    """
    Fetch the most or least frequent words across all files on the server.
    """
    if order not in ["dsc", "asc"]:
        typer.echo("Invalid order. Use 'dsc' for descending or 'asc' for ascending.")
        raise typer.Exit(code=1)

    response = requests.get(f"{BASE_URL}/freq-words", params={"n": n, "order": order})

    if response.status_code == 200:
        typer.echo("Frequent Words:")
        for word, count in response.json().get("words", []):
            typer.echo(f"{word}: {count}")
    else:
        typer.echo(f"Error: {response.text}")


if __name__ == "__main__":
    app()
