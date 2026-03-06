from importlib.metadata import PackageNotFoundError, version


def _resolve_version() -> str:
    try:
        return version("tidyup")
    except PackageNotFoundError:
        try:
            from setuptools_scm import get_version

            return get_version(root="..", relative_to=__file__)
        except Exception:
            return "0.0.2"


__version__ = _resolve_version()

def main():
    from .tidyup import main as _main

    return _main()

__all__ = ["main", "__version__"]
