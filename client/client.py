import typer
import requests
from pathlib import Path
from typing import List

app = typer.Typer()

SERVER_URL = "http://127.0.0.1:8000/upload"

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

    for file in files:
        if not file.exists():
            typer.echo(f"File '{file}' does not exist.")
            raise typer.Exit(code=1)  # File not exist locally
        file_data.append(("files", (file.name, file.open("rb"))))

    # Send files to the server
    response = requests.post(SERVER_URL, files=file_data)

    if response.status_code == 200:
        typer.echo("Files uploaded successfully!")
        # Details for each uploaded file
        for file_response in response.json():
            typer.echo(f"File: {file_response['file']} - {file_response['message']}")

    elif response.status_code == 400:  # If file already exists
        typer.echo(f"Error: {response.json()['detail']}")
        raise typer.Exit(code=1)  # Exit with non-zero code
    
    else:
        typer.echo(f"Unexpected error: {response.text}")
        raise typer.Exit(code=1)
    
@app.command()
def ls():
    """
    List all files stored on the server.
    """
    SERVER_URL = "http://127.0.0.1:8000/list"  # Endpoint

    response = requests.get(SERVER_URL)

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

if __name__ == "__main__":
    app()
