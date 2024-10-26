import os
import shutil
import sys
import re
from pathlib import Path
from datetime import datetime
import argparse

EXCLUDED_FILES = [
    ".Rproj", "requirements.txt", ".code-workspace",
    "package.json", "config.toml", "config.json", ".yaml"
]

def list_files(files_loc): return [f for f in files_loc.iterdir() if f.is_file() and re.match(r"^[^.][^/]*\.[a-zA-Z0-9]+$", f.name)]

def filter_files(files): return [f for f in files if f.name not in EXCLUDED_FILES and not any(f.name.endswith(ext) for ext in EXCLUDED_FILES)]

def create_directory(path):
    if not path.exists():
        path.mkdir(parents=True)

def move_file(file, dest_dir):
    dest_file = dest_dir / file.name
    shutil.move(str(file), str(dest_file))

def get_destination(file, order):
    parts = []
    for char in order:
        if char == 'e':
            parts.append(file.suffix[1:])
        elif char == 'd':
            modified_time = datetime.fromtimestamp(file.stat().st_mtime)
            parts.append(str(modified_time.year))
            parts.append(str(modified_time.month))

    return Path(*parts)

def tidy_files(files_loc, order):
    files = filter_files(list_files(files_loc))
    for file in files:
        dest_dir = files_loc / get_destination(file, order)
        create_directory(dest_dir)
        move_file(file, dest_dir)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Organize files by extension and/or date.",                             
        epilog="Examples:\n"
               "  tidyup -e /path/to/dir       Organize by extension\n"
               "  tidyup -d /path/to/dir       Organize by date\n"
               "  tidyup -ed /path/to/dir      Organize by extension and date\n"
               "  tidyup -de /path/to/dir      Organize by date and extension",
        formatter_class=argparse.RawDescriptionHelpFormatter
                                     )
    parser.add_argument("directory", type=str, help="Directory to organize")
    parser.add_argument("-e", action="store_true", help="Organize by extension")
    parser.add_argument("-d", action="store_true", help="Organize by date")
    return parser.parse_args()

def main():
    args = parse_arguments()
    files_loc = Path(args.directory)
    
    if not files_loc.is_dir():
        print(f"The path {files_loc} is not a directory or does not exist.")
        return

    order = sys.argv[1]

    if order:
        tidy_files(files_loc, order)
    else:
        print("No valid flags provided. Use -e, -d, -ed, or -de.")

if __name__ == "__main__":
    main()