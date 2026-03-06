from pathlib import Path

from .utils import parse_arguments, tidy_files


def main():
    args = parse_arguments()
    files_loc = Path(args.directory)

    if not files_loc.is_dir():
        print(f"The path {files_loc} is not a directory or does not exist.")
        return 1

    if args.rearrange:
        tidy_files(files_loc, args.order, recursive=True, depth=args.depth)
    else:
        tidy_files(files_loc, args.order)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
