import os
from datetime import datetime
from pathlib import Path

from tidyup.utils import discover_files, tidy_files


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


def test_tidy_files_recursive_skips_files_under_hidden_directories(tmp_path: Path):
    hidden_dir = tmp_path / ".hidden_dir"
    hidden_dir.mkdir()
    hidden_file = hidden_dir / "hidden.txt"
    visible_file = tmp_path / "visible.txt"
    hidden_file.write_text("hidden")
    visible_file.write_text("visible")

    tidy_files(tmp_path, "-e", recursive=True, depth=2)

    assert hidden_file.exists()
    assert (tmp_path / "txt" / "visible.txt").exists()


def test_tidy_files_recursive_skips_nested_files_under_hidden_directories(tmp_path: Path):
    nested_hidden_dir = tmp_path / ".hidden_dir" / "nested"
    nested_hidden_dir.mkdir(parents=True)
    hidden_file = nested_hidden_dir / "hidden.txt"
    visible_file = tmp_path / "visible.txt"
    hidden_file.write_text("hidden")
    visible_file.write_text("visible")

    tidy_files(tmp_path, "-e", recursive=True, depth=3)

    assert hidden_file.exists()
    assert (tmp_path / "txt" / "visible.txt").exists()


def test_discover_files_has_cross_mode_policy_parity_for_same_scope(tmp_path: Path):
    top_level = tmp_path / "top.txt"
    hidden = tmp_path / ".hidden"
    excluded = tmp_path / "requirements.txt"
    suffix_excluded = tmp_path / "settings.yaml"
    no_extension = tmp_path / "LICENSE"

    top_level.write_text("ok")
    hidden.write_text("hidden")
    excluded.write_text("reqs")
    suffix_excluded.write_text("yaml")
    no_extension.write_text("license")

    top_level_only = discover_files(tmp_path)
    recursive_same_scope = discover_files(tmp_path, recursive=True, depth=0)

    expected = [top_level]
    assert top_level_only == expected
    assert recursive_same_scope == expected


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


def test_tidy_files_recursive_collision_is_deterministic(tmp_path: Path, capsys):
    alpha = tmp_path / "alpha"
    beta = tmp_path / "beta"
    alpha.mkdir()
    beta.mkdir()

    first = alpha / "dup.txt"
    second = beta / "dup.txt"
    first.write_text("alpha")
    second.write_text("beta")

    tidy_files(tmp_path, "-e", recursive=True, depth=2)

    output = capsys.readouterr().out
    destination = tmp_path / "txt" / "dup.txt"

    assert destination.exists()
    assert destination.read_text() == "alpha"
    assert second.exists()
    assert (
        f"Skipping {second}: destination already contains dup.txt at {tmp_path / 'txt'}."
        in output
    )


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


def test_tidy_files_multi_extension_uses_final_suffix(tmp_path: Path):
    archive = tmp_path / "archive.tar.gz"
    archive.write_text("archive")

    tidy_files(tmp_path, "-e")

    assert (tmp_path / "gz" / "archive.tar.gz").exists()
