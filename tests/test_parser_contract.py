import pytest

from tidyup.utils import parse_arguments


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
