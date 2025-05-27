"""Convenient top-level imports for the Stormworkspy package."""

from .Stormworkspy import Stormworkspy
from . import sensors
from .sensors import *  # re-export sensor classes at package level

__all__ = ["Stormworkspy"] + sensors.__all__
__version__ = '0.1.0'
