# File Store Service

This is a simple file store service built with Python. It consists of:
1. A server-side application using FastAPI.
2. A command-line client to interact with the server.

## Features
- Add, update, delete, and list files.
- Perform operations like word count and finding frequent words.

## Tech Stack
- **FastAPI** for the server (lightweight and fast).
- **Python** for both server and client implementations.

## Installation

You can install the tool directly from GitHub using `pip` or `poetry`:

### Install with `pip`

To install the latest version of the CLI tool directly from GitHub:

```bash
pip install git+https://github.com/your-username/the-file-store.git
```

### Install with `poetry`

To add it as a dependency to your project:

```bash
poetry add git+https://github.com/your-username/the-file-store.git
```

### Install by Cloning the Repository
1. Clone the repository:

```bash
git clone https://github.com/your-username/the-file-store.git
```

2. Navigate to the project directory:
```bash
cd the-file-store
```

3. Install the dependencies using poetry:
```bash
poetry install
```

4. (Optional) If you want to use the tool globally, you can add it to your environment:
```bash
poetry run store [command]
```

## Usage
Once installed, you can run the tool from the command line:

```bash
store [command]
```

## Available Commands
- hello: Greet the server.
- add: Upload files to the server.
- ls: List all files stored on the server.
- rm: Remove a file from the store.
- update: Update a file on the server.
- wc: Get the total word count from all files stored.
- freq_words: Get the most or least frequent words across all files.