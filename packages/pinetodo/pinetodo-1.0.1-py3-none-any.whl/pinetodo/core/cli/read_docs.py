import os
from rich.console import Console
from rich.markdown import Markdown
from .download_pinedocs import get_opinedocs_path, download_opinedocs

console = Console()

def read_docs():
    docs_path = get_opinedocs_path()

    if not os.path.exists(docs_path):
        console.print("File '.pinetodo.opinedocs' not found. Downloading from the server...")
        download_opinedocs()

    if os.path.exists(docs_path):
        with open(docs_path, "r", encoding="utf-8") as f:
            content = f.read()
            console.print(Markdown(content))
    else:
        console.print("Failed to get the documentation!")
