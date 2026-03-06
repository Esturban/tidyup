import argparse
import shutil
from datetime import datetime
from pathlib import Path

EXCLUDED_FILES = [
    ".Rproj",
    "requirements.txt",
    ".code-workspace",
    "package.json",
    "config.toml",
    "config.json",
    ".yaml",
]

README_USAGE = "tidyup [-h] [-e] [-d] [-r] [-L DEPTH] directory"

USAGE_EXAMPLES = [
    ("tidyup -e /path/to/dir", "Organize by extension"),
    ("tidyup -d /path/to/dir", "Organize by date"),
    ("tidyup -ed /path/to/dir", "Organize by extension then date"),
    ("tidyup -de /path/to/dir", "Organize by date then extension"),
    ("tidyup -r -e /path/to/dir", "Recursive extension organize (default depth 2)"),
    ("tidyup -r -d /path/to/dir", "Recursive date organize (default depth 2)"),
    (
        "tidyup -r -L 3 -e /path/to/dir",
        "Recursive extension organize with explicit depth",
    ),
    ("tidyup -r -L 3 -d /path/to/dir", "Recursive date organize with explicit depth"),
]

SAFETY_NOTES = [
    "Dotfiles and excluded config/workspace files are skipped in all modes.",
    "Files are grouped by their final suffix, so archive.tar.gz is treated as .gz.",
    "Existing destination files are never overwritten; collisions are skipped and reported.",
]


class OrderedAxisAction(argparse.Action):
    """Capture axis flags in user-provided order while setting boolean attrs."""

    def __call__(self, parser, namespace, values, option_string=None):
        axis_order = getattr(namespace, "axis_order", [])
        axis_order.append(self.dest)
        setattr(namespace, "axis_order", axis_order)
        setattr(namespace, self.dest, True)


def is_eligible_file(file_path: Path) -> bool:
    if not file_path.is_file():
        return False

    # Hidden files are excluded by default.
    if file_path.name.startswith("."):
        return False

    if file_path.name in EXCLUDED_FILES:
        return False

    if any(file_path.name.endswith(ext) for ext in EXCLUDED_FILES):
        return False

    # Only organize files that have at least one extension.
    return bool(file_path.suffix)


def list_files(files_loc: Path) -> list[Path]:
    return sorted(
        (file_path for file_path in files_loc.iterdir() if is_eligible_file(file_path)),
        key=lambda file_path: file_path.name,
    )


def iter_recursive_files(files_loc: Path, depth: int) -> list[Path]:
    collected: list[Path] = []
    for file_path in files_loc.rglob("*"):
        if not file_path.is_file():
            continue

        relative_depth = len(file_path.relative_to(files_loc).parts) - 1
        if relative_depth > depth:
            continue

        if is_eligible_file(file_path):
            collected.append(file_path)

    return sorted(
        collected,
        key=lambda file_path: file_path.relative_to(files_loc).as_posix(),
    )


def discover_files(files_loc: Path, recursive: bool = False, depth: int = 2) -> list[Path]:
    return iter_recursive_files(files_loc, depth) if recursive else list_files(files_loc)


def create_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def get_destination(file_path: Path, order: str) -> Path:
    parts = []

    for char in order:
        if char == "e":
            parts.append(file_path.suffix[1:])
        elif char == "d":
            modified_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            parts.extend([str(modified_time.year), f"{modified_time.month:02d}"])

    return Path(*parts)


def move_file(file_path: Path, dest_dir: Path) -> tuple[bool, str | None]:
    target = dest_dir / file_path.name

    if file_path.resolve() == target.resolve():
        return False, f"Skipping {file_path}: already in destination."

    if target.exists():
        return False, (
            f"Skipping {file_path}: destination already contains {target.name} at {dest_dir}."
        )

    shutil.move(str(file_path), str(target))
    return True, None


def tidy_files(files_loc: Path, order: str, recursive: bool = False, depth: int = 2) -> None:
    all_files = discover_files(files_loc, recursive=recursive, depth=depth)

    for file_path in all_files:
        dest_dir = files_loc / get_destination(file_path, order)
        create_directory(dest_dir)
        moved, reason = move_file(file_path, dest_dir)
        if not moved and reason:
            print(reason)


def determine_order(axis_order: list[str]) -> str:
    return "-" + "".join(axis_order)


def validate_arguments(parser: argparse.ArgumentParser, args: argparse.Namespace) -> argparse.Namespace:
    axis_order = getattr(args, "axis_order", [])
    if not axis_order:
        parser.error("You must provide at least one organizing axis: -d and/or -e.")

    if args.depth is not None and not args.rearrange:
        parser.error("-L/--depth requires -r/--rearrange.")

    if args.rearrange and args.depth is None:
        args.depth = 2

    if args.depth is not None and args.depth < 0:
        parser.error("-L/--depth must be >= 0.")

    args.order = determine_order(axis_order)
    return args


def build_parser() -> argparse.ArgumentParser:
    examples = "\n".join(
        f"  {command:<40} {description}" for command, description in USAGE_EXAMPLES
    )
    safety_notes = "\n".join(f"  - {note}" for note in SAFETY_NOTES)
    parser = argparse.ArgumentParser(
        description="Organize files by extension and/or date.",
        usage=README_USAGE,
        epilog=f"Examples:\n{examples}\n\nSafety notes:\n{safety_notes}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("directory", type=str, help="Directory to organize")
    parser.add_argument(
        "-e",
        nargs=0,
        action=OrderedAxisAction,
        default=False,
        help="Organize by extension",
    )
    parser.add_argument(
        "-d",
        nargs=0,
        action=OrderedAxisAction,
        default=False,
        help="Organize by date",
    )
    parser.add_argument(
        "-r", "--rearrange", action="store_true", help="Rearrange files recursively"
    )
    parser.add_argument(
        "-L", "--depth", type=int, help="Depth of subdirectory traversal"
    )
    return parser


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    parser = build_parser()
    args = parser.parse_args(argv)
    return validate_arguments(parser, args)
