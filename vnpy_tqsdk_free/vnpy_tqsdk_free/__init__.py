import importlib_metadata

from .tqsdk_free_datafeed import TqsdkDatafeed as Datafeed


try:
    __version__ = importlib_metadata.version("vnpy_tqsdk_free")
except importlib_metadata.PackageNotFoundError:
    __version__ = "dev"
