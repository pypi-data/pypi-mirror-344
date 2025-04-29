"""
cf-plot: code-light plotting for earth science and aligned research

Documentation is hosted and found at: https://ncas-cms.github.io/cf-plot/
"""

__author__ = "Sadie Bartholomew, Andy Heaps"
__maintainer__ ="Sadie Bartholomew"
__date__ = "28th April 2025"
__version__ = "3.4.0"

from .cfplot import *  # noqa: F403, F401

# Internal-use methods required for testing
from .cfplot import _gvals
from .cfplot import _mapaxis
from .cfplot import _which
