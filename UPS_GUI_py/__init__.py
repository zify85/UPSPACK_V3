"""
UPS GUI Package for UPSPACK V3

This package provides classes and utilities for interfacing with the UPSPACK V3
UPS system, including UART communication and GPIO monitoring functionality.
"""

from .upspackv2 import UPS2, UPS2_IO

__version__ = "1.0.0"
__author__ = "UPSPACK V3"
__all__ = ["UPS2", "UPS2_IO"]
