"""
qvalue
Calculates the fraction of native contacts conserved during the simulation.
"""

# Add imports here
from importlib.metadata import version, PackageNotFoundError

try:
    # pip installation
    __version__ = version("md-qvalue")
except PackageNotFoundError:
    try:
        # local installation (e.g., `import qvalue`)
        __version__ = version("qvalue")
    except PackageNotFoundError:
        __version__ = "unknown"

from qvalue.qvalue import qValue

__all__ = ['qvalue']