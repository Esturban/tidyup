import sys
from importlib.metadata import PackageNotFoundError

from tidyup import __version__, _resolve_version
from tidyup.utils import build_parser


def test_resolve_version_fallback(monkeypatch):
    monkeypatch.setattr(
        "tidyup.version", lambda _: (_ for _ in ()).throw(PackageNotFoundError())
    )
    monkeypatch.setitem(sys.modules, "setuptools_scm", None)
    assert _resolve_version() == "0.0.2"


def test_version_is_non_empty_string():
    assert isinstance(__version__, str)
    assert __version__


def test_help_includes_recursive_and_order_examples():
    help_text = build_parser().format_help()
    assert "-r, --rearrange" in help_text
    assert "-L DEPTH" in help_text or "-L, --depth" in help_text
    assert "-ed" in help_text
    assert "-de" in help_text
    assert "tidyup -r -e /path/to/dir" in help_text
    assert "tidyup -r -L 3 -e /path/to/dir" in help_text
    assert "tidyup -r -L 3 -d /path/to/dir" in help_text
    assert "Dotfiles and excluded config/workspace files are skipped in all modes." in help_text
    assert "archive.tar.gz is treated as .gz" in help_text
    assert "Existing destination files are never overwritten" in help_text
