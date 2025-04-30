from importlib.metadata import version, PackageNotFoundError

from . import helper
from .pytrate import CombinedSiteAaModel, CrossedSiteAaModel
from .foldchange import FoldChangeModel

try:
    __version__ = version("pytrate")
except PackageNotFoundError:
    __version__ = "unknown"


__all__ = [
    "CombinedSiteAaModel",
    "CrossedSiteAaModel",
    "FoldChangeModel",
    "helper",
    "__version__",
]
