"""Utility functions for QRCodeX."""

import re
from typing import Union, Tuple
from pathlib import Path
import base64
from PIL import Image
from .exceptions import QRCodeXValueError, QRCodeXTypeError, QRCodeXImageError, QRCodeXFileError

def validate_color(color: str) -> str:
    """
    Validate and normalize color format.
    
    Args:
        color: Color in hex, RGB, or named format
        
    Returns:
        Normalized color string
        
    Raises:
        QRCodeXValueError: If color format is invalid
    """
    if not isinstance(color, str):
        raise QRCodeXTypeError("Color must be a string")
    
    # Hex color
    if re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
        return color.lower()
    
    # RGB/RGBA color
    if re.match(r'^rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*(?:,\s*[\d.]+)?\s*\)$', color):
        # Validate RGB values are in range
        try:
            values = [int(x.strip()) for x in color[color.find('(') + 1:color.find(')')].split(',')[:3]]
            if not all(0 <= x <= 255 for x in values):
                raise QRCodeXValueError(f"RGB values must be between 0 and 255: {color}")
        except ValueError:
            raise QRCodeXValueError(f"Invalid RGB format: {color}")
        return color
    
    # Named color
    valid_colors = {
        'black', 'white', 'red', 'green', 'blue', 'yellow', 'purple', 'orange',
        'gray', 'grey', 'brown', 'pink', 'cyan', 'magenta', 'lime', 'maroon',
        'navy', 'olive', 'teal', 'aqua', 'fuchsia', 'silver'
    }
    if color.lower() in valid_colors:
        return color.lower()
    
    raise QRCodeXValueError(f"Invalid color format: {color}")

def validate_size(size: Union[int, float]) -> int:
    """
    Validate and normalize size value.
    
    Args:
        size: Size value to validate
        
    Returns:
        Normalized integer size
        
    Raises:
        QRCodeXValueError: If size is invalid
    """
    if not isinstance(size, (int, float)):
        raise QRCodeXTypeError("Size must be a number")
    
    size_int = int(size)
    if size_int <= 0:
        raise QRCodeXValueError("Size must be positive")
    
    return size_int

def validate_path(path: Union[str, Path]) -> Path:
    """
    Validate and normalize file path.
    
    Args:
        path: Path to validate
        
    Returns:
        Normalized Path object
        
    Raises:
        QRCodeXFileError: If path is invalid
    """
    try:
        return Path(path).resolve()
    except Exception as e:
        raise QRCodeXFileError(f"Invalid path: {path}") from e

def image_to_data_uri(image_path: Union[str, Path]) -> str:
    """
    Convert image to data URI.
    
    Args:
        image_path: Path to image file
        
    Returns:
        Data URI string
        
    Raises:
        QRCodeXImageError: If image cannot be converted
    """
    try:
        path = validate_path(image_path)
        if not path.exists():
            raise QRCodeXFileError(f"Image file not found: {path}")
        
        with Image.open(path) as img:
            img_format = img.format.lower()
            if img_format not in {'png', 'jpeg', 'jpg', 'gif'}:
                raise QRCodeXImageError(f"Unsupported image format: {img_format}")
            
            img_data = path.read_bytes()
            b64_data = base64.b64encode(img_data).decode('ascii')
            return f"data:image/{img_format};base64,{b64_data}"
    except Exception as e:
        raise QRCodeXImageError(f"Failed to convert image to data URI: {e}") from e

def detect_data_type(data: str) -> str:
    """
    Detect the type of data.
    
    Args:
        data: Data string to analyze
        
    Returns:
        Detected data type ('text', 'url', 'email', 'phone', 'wifi', 'geo')
    """
    # URL pattern
    if re.match(r'^https?://[\w\-\.]+(:\d+)?(/[\w\-\./?%&=]*)?$', data):
        return 'url'
    
    # Email pattern
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data):
        return 'email'
    
    # Phone pattern
    if re.match(r'^\+?[\d\s\-\(\)]+$', data):
        return 'phone'
    
    # WiFi pattern
    if re.match(r'^WIFI:T:[\w\-]+;S:[\w\-]+;P:[\w\-]+;;$', data):
        return 'wifi'
    
    # Geo pattern
    if re.match(r'^geo:-?\d+\.\d+,-?\d+\.\d+$', data):
        return 'geo'
    
    return 'text' 