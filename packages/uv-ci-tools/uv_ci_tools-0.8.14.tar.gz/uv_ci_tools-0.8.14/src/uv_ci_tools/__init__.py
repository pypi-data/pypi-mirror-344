import importlib.metadata
import pathlib

__version__ = importlib.metadata.version(pathlib.Path(__file__).parent.name)
