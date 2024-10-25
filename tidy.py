import os
import sys
import shutil
import re
from pathlib import Path

def main(files_loc):
    files_loc = Path(files_loc)
    
    if not files_loc.is_dir():
        print(f"The path {files_loc} is not a directory or does not exist.")
        return

    # List of files to be filtered out
    excluded_files = [
        ".Rproj", "requirements.txt", ".code-workspace",
        "package.json", "config.toml", "config.json", ".yaml"
    ]
    
    # List all files in the directory matching the pattern
    all_files = [f for f in files_loc.iterdir() if f.is_file() and re.match(r"^[^.][^/]*\.[a-zA-Z0-9]+$", f.name)]
    # Filter out excluded files
    filtered_files = [f for f in all_files if f.name not in excluded_files and not any(f.name.endswith(ext) for ext in excluded_files)]
    # Get unique file extensions
    file_types = set(f.suffix[1:] for f in filtered_files if f.suffix)
    
    for file_type in file_types:
        type_dir = files_loc / file_type
        # Create directory for the file type if it doesn't exist
        if not type_dir.exists():
            type_dir.mkdir()

        files_loc_type = [f for f in filtered_files if f.suffix[1:] == file_type]
        for file in files_loc_type:
            dest_file = type_dir / file.name
            shutil.move(str(file), str(dest_file))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clean.py <directory/path/selected>")
    else:
        main(sys.argv[1])
