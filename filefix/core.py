import typer
import os
from typing import Dict, Union
from pathlib import Path
from datetime import datetime
from rich import print

app = typer.Typer(help="A CLI tool to organize files in a directory.")

FILE_CATEGORIES = {
    ".jpg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".jpeg": "Images",

    ".avi": "Videos",
    ".mov": "Videos",

    ".pdf": "PDFs",
    ".txt": "Text",
    ".docx": "Word",
    ".xlsx": "Excel",
    ".pptx": "PowerPoint",
    ".ppt": "PowerPoint",
    ".csv": "CSV",

    ".mp3": "Music",
    ".wav": "Music",
    ".flac": "Music",

    ".mp4": "Videos",
    ".webm": "Videos",
    ".webp": "Videos",
    ".mov":"Videos",

    # Languages 
    ".py": "Python",
    ".java": "Java",
    ".c": "C",
    ".cpp": "C++",
    ".js": "WEB",
    ".html": "WEB",
    ".css": "WEB", 
    ".zip": "Archives",
    
    ".rar": "Archives",
    ".tar": "Archives",

    ".exe": "Executables",
    ".torrent": "Torrents",
    ".t":"TOR",

    ".app": "Applications",
    ".apk": "Applications",
}

# org
@app.command()
def organize(directory: str = typer.Argument(".", help="Directory to organize")):
    """Organize files in a directory based on their file type."""

    if not os.path.isdir(directory):
        typer.echo(f"Error: '{directory}' is not a valid directory.")
        raise typer.Exit(code=1)


    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            
            _, ext = os.path.splitext(filename)
            ext = ext.lower()
            
            target_folder = FILE_CATEGORIES.get(ext, "Others")
            target_path = os.path.join(directory, target_folder)
            
            os.makedirs(target_path, exist_ok=True)
            
            new_path = os.path.join(target_path, filename)
            try:
                os.rename(file_path, new_path)
                typer.echo(f"Moved '{filename}' to '{target_folder}'")
                print(f"Moved '{filename}' to '{target_folder}'")
            except OSError as e:
                typer.echo(f"Error moving '{filename}': {e}")
                print(f"Error moving '{filename}': {e}")




#list categ
@app.command()
def list_categories():
    """List all file categories and their extensions."""
    categories = {}
    for ext, cat in FILE_CATEGORIES.items():
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(ext)
    
    typer.echo("📁 File Categories:")
    for category, extensions in sorted(categories.items()):
        typer.echo(f"  {category}: {', '.join(extensions)}")

