"""
QRCodeX - Advanced QR Code Generator

This module provides a powerful and flexible QR code generator with support for
multiple data types, custom styling, and various output formats.
"""

from .generator import QRCodeX
from .exceptions import QRCodeXError
from .capacity import ErrorCorrectionLevel

__version__ = "0.1.1"
__author__ = "Gamingop"
__email__ = "samratkafle36@gmail.com"

__all__ = ["QRCodeX", "QRCodeXError", "ErrorCorrectionLevel"]

# Re-export main class with proper docstring
class QRCodeX(QRCodeX):
    """Advanced QR Code Generator with multiple data type support.

    This class extends the basic QR code functionality with support for:
    - Multiple data types (text, URLs, images, binary)
    - Custom styling (colors, size, border)
    - Various output formats (PNG, SVG)
    - Error correction levels
    
    Attributes:
        error_correction (str): Error correction level ('L', 'M', 'Q', 'H')
        box_size (int): Size of each QR code module in pixels
        border (int): Border size in modules
        version (int, optional): QR code version (1-40), or None for auto

    Example:
        >>> qr = QRCodeX()
        >>> qr.add_data("Hello, World!")
        >>> qr.generate("output.png")
    """ 