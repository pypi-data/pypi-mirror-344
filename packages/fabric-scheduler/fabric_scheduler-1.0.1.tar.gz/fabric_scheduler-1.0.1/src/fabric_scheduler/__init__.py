"""
Fabric Scheduler Package.

This package provides functionality to schedule Fabric artifacts (Notebooks, Dataflows, Pipelines)
using the Fabric REST API.
"""
import sys

if sys.version_info[:2] >= (3, 8):
    # Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

# Import main classes for direct package access
from .core._core import ArtifactScheduler

__all__ = ["ArtifactScheduler", "__version__"]
