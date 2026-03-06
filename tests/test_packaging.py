import subprocess
import sys
from importlib.metadata import PackageNotFoundError

from tidyup import FALLBACK_VERSION, __version__, _resolve_version


def test_resolve_version_fallback(monkeypatch):
    monkeypatch.setattr(
        "tidyup.version", lambda _: (_ for _ in ()).throw(PackageNotFoundError())
    )
    monkeypatch.setitem(sys.modules, "setuptools_scm", None)
    assert _resolve_version() == FALLBACK_VERSION


def test_fallback_version_tracks_next_release_target():
    assert FALLBACK_VERSION == "0.0.4"


def test_version_is_non_empty_string():
    assert isinstance(__version__, str)
    assert __version__


def test_python_m_tidyup_help_runs():
    process = subprocess.run(
        [sys.executable, "-m", "tidyup", "-h"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert process.returncode == 0
    assert "Organize files by extension and/or date." in process.stdout
    assert "tidyup [-h] [-e] [-d] [-r] [-L DEPTH] directory" in process.stdout
