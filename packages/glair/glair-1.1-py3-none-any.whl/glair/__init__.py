# glair/__init__.py

# Make the package behave like main.py when doing "import glair"
from .main import *

# Explicitly expose processing and model as submodules
from . import processing
from . import model

# Optional (good practice): define __all__ to control public API
__all__ = []

# Dynamically extend __all__ to include things from main.py
try:
    from .main import __all__ as main_all
    __all__.extend(main_all)
except ImportError:
    pass

# Add processing and model to __all__ for "from glair import *" safety
__all__.extend(["processing", "model"])

