from importlib.metadata import PackageNotFoundError, version

FALLBACK_VERSION = "0.0.4"


def _resolve_version() -> str:
    try:
        return version("tidyup")
    except PackageNotFoundError:
        try:
            from setuptools_scm import get_version

            return get_version(root="..", relative_to=__file__)
        except Exception:
            return FALLBACK_VERSION


__version__ = _resolve_version()

def main():
    from .tidyup import main as _main

    return _main()

__all__ = ["main", "__version__"]
