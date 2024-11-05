import argparse
import shutil
import re
import os 
from pathlib import Path
from datetime import datetime

EXCLUDED_FILES = [
    ".Rproj", "requirements.txt", ".code-workspace",
    "package.json", "config.toml", "config.json", ".yaml"
]
#List all of the files in the selected location
def list_files(files_loc): return [f for f in files_loc.iterdir() if f.is_file() and re.match(r"^[^.][^/]*\.[a-zA-Z0-9]+$", f.name)]
#Filter out the excluded files
def filter_files(files): return [f for f in files if f.name not in EXCLUDED_FILES and not any(f.name.endswith(ext) for ext in EXCLUDED_FILES)]
#Create the directories
def create_directory(path): path.mkdir(parents=True) if not path.exists() else None
#Move the files from the selected to the output directory
def move_file(file, dest_dir): shutil.move(str(file), str(dest_dir / file.name))
#Get the destination directory
def get_destination(file, order):
    parts = []
    for char in order:
        if char == 'e': parts.append(file.suffix[1:])
        elif char == 'd':
            modified_time = datetime.fromtimestamp(file.stat().st_mtime)
            parts.extend([str(modified_time.year), str(modified_time.month)])
    return Path(*parts)
#Tidy the files by extension and/or date
def tidy_files(files_loc, order, recursive=False, depth=2):
    all_files = []
    if recursive:
        for root, _, files in os.walk(files_loc):
            if Path(root).relative_to(files_loc).parts and len(Path(root).relative_to(files_loc).parts) > depth:
                continue
            for file in files:
                file_path = Path(root) / file
                if file_path.is_file() and file_path.name not in EXCLUDED_FILES:
                    all_files.append(file_path)
    else:
        all_files = filter_files(list_files(files_loc))
    
    for file in all_files:
        dest_dir = files_loc / get_destination(file, order)
        create_directory(dest_dir)
        move_file(file, dest_dir)
#Parse the arguments from the command line and return the verbose on error
def parse_arguments():
    parser = argparse.ArgumentParser(description="Organize files by extension and/or date.",                             
        epilog="Examples:\n"
               "  tidyup -e /path/to/dir       Organize by extension\n"
               "  tidyup -d /path/to/dir       Organize by date\n"
               "  tidyup -ed /path/to/dir      Organize by extension and date\n"
               "  tidyup -de /path/to/dir      Organize by date and extension\n"
               "  tidyup -r -d  -L 2 /path/to/dir       Rearrange files recursively",
        formatter_class=argparse.RawDescriptionHelpFormatter
                                     )
    parser.add_argument("directory", type=str, help="Directory to organize")
    parser.add_argument("-e", action="store_true", help="Organize by extension")
    parser.add_argument("-d", action="store_true", help="Organize by date")
    parser.add_argument("-r", "--rearrange", action="store_true", help="Rearrange files recursively")
    parser.add_argument("-L","--depth", type=int, help="Depth of subdirectory traversal")
   
    return parser.parse_args()
