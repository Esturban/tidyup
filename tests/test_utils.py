import os
from datetime import datetime
from pathlib import Path

import pytest

from tidyup.utils import parse_arguments, tidy_files


def test_parse_arguments_accepts_locked_contract_combinations():
    expected = [
        (["-e", "/path/to/dir"], "-e", False, None),
        (["-d", "/path/to/dir"], "-d", False, None),
        (["-ed", "/path/to/dir"], "-ed", False, None),
        (["-de", "/path/to/dir"], "-de", False, None),
        (["-r", "-e", "/path/to/dir"], "-e", True, 2),
        (["-r", "-d", "/path/to/dir"], "-d", True, 2),
        (["-r", "-L", "3", "-e", "/path/to/dir"], "-e", True, 3),
        (["-r", "-L", "3", "-d", "/path/to/dir"], "-d", True, 3),
    ]

    for argv, order, recursive, depth in expected:
        args = parse_arguments(argv)
        assert args.order == order
        assert args.rearrange is recursive
        assert args.depth == depth


def test_parse_arguments_extension():
    args = parse_arguments(["-e", "/path/to/dir"])
    assert args.e is True
    assert args.d is False
    assert args.rearrange is False
    assert args.directory == "/path/to/dir"
    assert args.depth is None
    assert args.order == "-e"


def test_parse_arguments_date():
    args = parse_arguments(["-d", "/path/to/dir"])
    assert args.e is False
    assert args.d is True
    assert args.rearrange is False
    assert args.directory == "/path/to/dir"
    assert args.depth is None
    assert args.order == "-d"


def test_parse_arguments_preserves_order():
    args_de = parse_arguments(["-de", "/path/to/dir"])
    args_ed = parse_arguments(["-ed", "/path/to/dir"])

    assert args_de.order == "-de"
    assert args_ed.order == "-ed"


def test_parse_arguments_recursive_default_depth():
    args = parse_arguments(["-r", "-d", "/path/to/dir"])
    assert args.rearrange is True
    assert args.depth == 2


def test_parse_arguments_recursive_explicit_depth():
    args = parse_arguments(["-r", "-e", "-L", "4", "/path/to/dir"])
    assert args.depth == 4


def test_parse_arguments_rejects_depth_without_recursive(capsys):
    with pytest.raises(SystemExit) as exc_info:
        parse_arguments(["-L", "3", "-e", "/path/to/dir"])

    assert exc_info.value.code == 2
    assert "requires -r/--rearrange" in capsys.readouterr().err


def test_parse_arguments_rejects_missing_axis(capsys):
    with pytest.raises(SystemExit) as exc_info:
        parse_arguments(["/path/to/dir"])

    assert exc_info.value.code == 2
    assert "at least one organizing axis" in capsys.readouterr().err


def test_parse_arguments_rejects_negative_depth(capsys):
    with pytest.raises(SystemExit) as exc_info:
        parse_arguments(["-r", "-d", "-L", "-1", "/path/to/dir"])

    assert exc_info.value.code == 2
    assert "must be >= 0" in capsys.readouterr().err


def test_tidy_files_dotfiles_and_excluded_are_skipped(tmp_path: Path):
    (tmp_path / "visible.txt").write_text("ok")
    (tmp_path / ".env").write_text("secret")
    (tmp_path / "requirements.txt").write_text("pkg")

    tidy_files(tmp_path, "-e")

    assert (tmp_path / "txt" / "visible.txt").exists()
    assert (tmp_path / ".env").exists()
    assert (tmp_path / "requirements.txt").exists()


def test_tidy_files_recursive_uses_same_exclusion_rules(tmp_path: Path):
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "data.txt").write_text("ok")
    (nested / ".hidden.txt").write_text("hidden")
    (nested / "config.json").write_text("cfg")

    tidy_files(tmp_path, "-e", recursive=True, depth=2)

    assert (tmp_path / "txt" / "data.txt").exists()
    assert (nested / ".hidden.txt").exists()
    assert (nested / "config.json").exists()


def test_tidy_files_enforces_depth_boundary(tmp_path: Path):
    deep = tmp_path / "a" / "b" / "c"
    deep.mkdir(parents=True)
    shallow_file = tmp_path / "a" / "shallow.txt"
    deep_file = deep / "deep.txt"
    shallow_file.write_text("s")
    deep_file.write_text("d")

    tidy_files(tmp_path, "-e", recursive=True, depth=1)

    assert (tmp_path / "txt" / "shallow.txt").exists()
    assert deep_file.exists()


def test_tidy_files_collision_skips_and_reports(tmp_path: Path, capsys):
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    source_file = source_dir / "dup.txt"
    source_file.write_text("from source")

    destination_dir = tmp_path / "txt"
    destination_dir.mkdir()
    destination_file = destination_dir / "dup.txt"
    destination_file.write_text("already there")

    tidy_files(tmp_path, "-e", recursive=True, depth=2)

    output = capsys.readouterr().out
    assert "destination already contains" in output
    assert source_file.exists()
    assert destination_file.read_text() == "already there"


def test_tidy_files_order_sensitivity_between_de_and_ed(tmp_path: Path):
    timestamp = datetime(2025, 1, 15, 9, 0, 0).timestamp()
    de_root = tmp_path / "de"
    ed_root = tmp_path / "ed"
    de_root.mkdir()
    ed_root.mkdir()

    de_file = de_root / "example.txt"
    ed_file = ed_root / "example.txt"
    de_file.write_text("de")
    ed_file.write_text("ed")

    de_file.touch()
    ed_file.touch()
    os.utime(de_file, (timestamp, timestamp))
    os.utime(ed_file, (timestamp, timestamp))

    tidy_files(de_root, "-de")
    tidy_files(ed_root, "-ed")

    assert (de_root / "2025" / "01" / "txt" / "example.txt").exists()
    assert (ed_root / "txt" / "2025" / "01" / "example.txt").exists()
    assert not (de_root / "txt" / "2025" / "01" / "example.txt").exists()
    assert not (ed_root / "2025" / "01" / "txt" / "example.txt").exists()
