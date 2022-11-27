"""Utility functions."""
from functools import lru_cache
from pathlib import Path


@lru_cache(None)
def get_package_dir() -> Path:
    """Return root directory of package."""
    return Path(__file__).resolve().parent
