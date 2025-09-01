import yaml
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
#empty rmv
@app.command()
def clean(directory: str = typer.Argument(".", help="Directory to clean empty folders from")):
    """Directory to clean empty folders from """
    if not os.path.isdir(directory):
        typer.echo(f"Error: '{directory}' is not a valid directory.")
        raise typer.Exit(code=1)

    for root, dirs, _ in os.walk(directory, topdown=False):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            try:
                if not os.listdir(folder_path):  # Check if folder is empty
                    os.rmdir(folder_path)
                    typer.echo(f"Deleted empty folder: '{folder_path}'")
            except OSError as e:
                typer.echo(f"Error deleting '{folder_path}': {e}")



#add category 
@app.command()
def add_category( 
    category_name: str = typer.Argument(..., help="Name of the category"),
    extension: str = typer.Argument(..., help="Extension of the category")
):
    """Add a new file category."""
    FILE_CATEGORIES[extension] = category_name
    typer.echo(f"Added category '{category_name}' with extension '{extension}'")


# stats
@app.command()
def stats(directory: str = typer.Argument(".", help="Directory to get stats from")):
    """Directory to get stats from"""
    if not os.path.isdir(directory):
        typer.echo(f"Error: '{directory}' is not a valid directory.")
        raise typer.Exit(code=1)

    total_files = 0
    file_types = {}
    size=0

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(filename)
            ext = ext.lower()
            
            total_files += 1
            size+=os.path.getsize(file_path)
            if ext in file_types:
                file_types[ext] += 1
            else:
                file_types[ext] = 1
    
    typer.echo(f"Total files: {total_files}")
    typer.echo(f"Total size: {size}")
    for ext, count in file_types.items():
        typer.echo(f"  {ext}: {count}")





#yaml
@app.command()
def create_structure(
    template_path: str = typer.Argument(..., help="Path to the YAML template file"),
    target_dir: str = typer.Argument(
        ".", 
        help="Directory where the structure will be created"
    ),
    force: bool = typer.Option(
        False, 
        "--force", "-f",
        help="Overwrite existing files and directories"
    )
):
    """
    Create a folder structure based on a YAML template.
    
    The YAML template should define the folder structure like this:
    
    project_name/:
      README.md: |
        # Project Title
        Created on: {{date}}
      src/:
        _init_.py: ""
        main.py: |
          def main():
              print("Hello, World!")
      tests/:
        _init_.py: ""
        test_main.py: ""
    """
    try:
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
            
        
        template_vars = {
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        
        for var, value in template_vars.items():
            template = template.replace(f'{{{{{var}}}}}', value)
            
        
        structure = yaml.safe_load(template)
        
        if not structure:
            typer.echo("Error: Empty or invalid YAML template")
            raise typer.Exit(1)
            
        target_path = Path(target_dir).resolve()
        target_path.mkdir(parents=True, exist_ok=True)
        
        created = process_structure(structure, target_path, force)
        
        typer.echo(f"\n✅ Successfully created {created['files']} files and {created['folders']} folders in {target_path}")
        
    except FileNotFoundError:
        typer.echo(f"Error: Template file not found: {template_path}")
        raise typer.Exit(1)
    except yaml.YAMLError as e:
        typer.echo(f"Error parsing YAML template: {e}")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"An error occurred: {e}")
        raise typer.Exit(1)


def process_structure(structure: Union[Dict, str], base_path: Path, force: bool) -> Dict[str, int]:
    counts = {'files': 0, 'folders': 0}
    
    if isinstance(structure, str):
        base_path.parent.mkdir(parents=True, exist_ok=True)
        
        if base_path.exists() and not force:
            typer.echo(f"Skipping existing file (use --force to overwrite): {base_path}")
            return counts
            
        base_path.write_text(structure, encoding='utf-8')
        typer.echo(f"Created file: {base_path}")
        counts['files'] = 1
        return counts
        
    for name, content in structure.items():
        if name.endswith('/'):
            name = name.rstrip('/')
            is_dir = True
        else:
            is_dir = content and isinstance(content, dict)
            
        item_path = base_path / name
        
        if is_dir:
           
            try:
                item_path.mkdir(exist_ok=force)
                if not item_path.exists() or force:
                    typer.echo(f"Created directory: {item_path}")
                    counts['folders'] += 1
                
                
                if content:
                    sub_counts = process_structure(content, item_path, force)
                    counts['files'] += sub_counts['files']
                    counts['folders'] += sub_counts['folders']
                    
            except FileExistsError:
                typer.echo(f"Skipping existing directory (use --force to overwrite): {item_path}")
                
        else:
             
            try:
                if item_path.exists() and not force:
                    typer.echo(f"Skipping existing file (use --force to overwrite): {item_path}")
                    continue
                    
                
                item_path.parent.mkdir(parents=True, exist_ok=True)
                
                
                if content is None:
                    content = ""
                item_path.write_text(str(content), encoding='utf-8')
                typer.echo(f"Created file: {item_path}")
                counts['files'] += 1
                
            except Exception as e:
                typer.echo(f"Error creating file {item_path}: {e}")
    
    return counts




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






# restore
@app.command()
def undo_organize(directory: str = typer.Argument(".", help="Directory to undo organize from")):
    """Directory to undo organize from"""
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
            except OSError as e:
                typer.echo(f"Error moving '{filename}': {e}")







if __name__ == "__main__":
    app()