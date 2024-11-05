from .utils import parse_arguments, tidy_files
import sys
from pathlib import Path

def main():
    args = parse_arguments()
    files_loc = Path(args.directory)
    
    if not files_loc.is_dir():
        print(f"The path {files_loc} is not a directory or does not exist.")
        return
    
    order = ""
    for arg in sys.argv[1:]:
        if arg in ["-d", "-e", "-de", "-ed"]:
            order = arg
            break
    
    if not order:
        print("No valid flags provided. Use -e, -d, -ed, -de, or -r.")
        sys.exit(1)
    
    if (args.rearrange and args.depth is None) or (args.depth is not None and not args.rearrange):
        print("Error: -r must be accompanied by -L, and -L must be accompanied by -r.")
        sys.exit(1)
    
    
    tidy_files(files_loc, order, recursive=True, depth=args.depth) if args.rearrange else tidy_files(files_loc, order)

if __name__ == "__main__":
    main()