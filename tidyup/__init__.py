# __init__.py
from setuptools_scm import get_version
try:
    __version__ = get_version()
except Exception:
    __version__ = "0.0.1"

from .tidyup import main