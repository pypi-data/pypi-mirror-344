"""
This module attempts to retrieve and set the version of the current package.
It uses `importlib.metadata.version` to get the version of the package based on the package name.
If the package is not found, it sets the version to "unknown".
Attributes:
    DIST_NAME (str): The name of the current package.
    __version__ (str): The version of the current package. If the package is not found, it is set to "unknown".
Exceptions:
    PackageNotFoundError: Raised when the package version cannot be found.
Cleanup:
    The imported `version` and `PackageNotFoundError` are deleted from the namespace after use.
"""

from importlib.metadata import PackageNotFoundError, version

from .collect_dep_modules import collect_package_dependencies
from .collect_pyd_modules import collect_pyd_modules_from_venv

try:
    DIST_NAME = __name__
    __version__ = version(DIST_NAME)
except PackageNotFoundError:
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

LOGGER_NAME = "python_build_utils"


__all__ = ["collect_package_dependencies", "collect_pyd_modules_from_venv"]
