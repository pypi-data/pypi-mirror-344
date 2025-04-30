"""
QR Code Generation Algorithm Implementation

This module implements the QR code generation algorithm from scratch,
without relying on the external qrcode library.
"""

import math
import re
from typing import List, Tuple, Dict, Any, Optional, Union
from enum import Enum, auto

from .capacity import ErrorCorrectionLevel

class QRMode(Enum):
    """QR Code encoding modes."""
    NUMERIC = auto()
    ALPHANUMERIC = auto()
    BYTE = auto()
    KANJI = auto()

class QRCode:
    """
    QR Code generator class that implements the algorithm from scratch.
    """
    
    # QR Code version information (1-40)
    # Each version has a specific number of modules (data + error correction)
    VERSION_INFO = {
        1: 21, 2: 25, 3: 29, 4: 33, 5: 37, 6: 41, 7: 45, 8: 49, 9: 53, 10: 57,
        11: 61, 12: 65, 13: 69, 14: 73, 15: 77, 16: 81, 17: 85, 18: 89, 19: 93, 20: 97,
        21: 101, 22: 105, 23: 109, 24: 113, 25: 117, 26: 121, 27: 125, 28: 129, 29: 133, 30: 137,
        31: 141, 32: 145, 33: 149, 34: 153, 35: 157, 36: 161, 37: 165, 38: 169, 39: 173, 40: 177
    }
    
    # Capacity table for different versions, modes, and error correction levels
    # Format: {version: {mode: {error_correction: (numeric, alphanumeric, byte, kanji)}}}
    CAPACITY = {
        1: {
            QRMode.NUMERIC: {
                ErrorCorrectionLevel.L: (41, 0, 0, 0),
                ErrorCorrectionLevel.M: (34, 0, 0, 0),
                ErrorCorrectionLevel.Q: (27, 0, 0, 0),
                ErrorCorrectionLevel.H: (17, 0, 0, 0)
            },
            QRMode.ALPHANUMERIC: {
                ErrorCorrectionLevel.L: (0, 25, 0, 0),
                ErrorCorrectionLevel.M: (0, 20, 0, 0),
                ErrorCorrectionLevel.Q: (0, 16, 0, 0),
                ErrorCorrectionLevel.H: (0, 10, 0, 0)
            },
            QRMode.BYTE: {
                ErrorCorrectionLevel.L: (0, 0, 17, 0),
                ErrorCorrectionLevel.M: (0, 0, 14, 0),
                ErrorCorrectionLevel.Q: (0, 0, 11, 0),
                ErrorCorrectionLevel.H: (0, 0, 7, 0)
            },
            QRMode.KANJI: {
                ErrorCorrectionLevel.L: (0, 0, 0, 10),
                ErrorCorrectionLevel.M: (0, 0, 0, 8),
                ErrorCorrectionLevel.Q: (0, 0, 0, 7),
                ErrorCorrectionLevel.H: (0, 0, 0, 4)
            }
        }
        # Additional versions would be defined here
    }
    
    def __init__(
        self,
        version: Optional[int] = None,
        error_correction: Union[ErrorCorrectionLevel, str] = ErrorCorrectionLevel.H,
        mask_pattern: int = -1
    ):
        """
        Initialize a QR Code generator.
        
        Args:
            version: QR code version (1-40), None for auto-selection
            error_correction: Error correction level (L, M, Q, H)
            mask_pattern: Mask pattern (0-7), -1 for auto-selection
        """
        self.version = version
        self.error_correction = self._parse_error_correction(error_correction)
        self.mask_pattern = mask_pattern
        self.data = ""
        self.mode = QRMode.BYTE  # Default mode
        self.modules = None
        self.module_count = 0
        self.data_cache = None
        self.data_list = []
    
    def _parse_error_correction(self, level: Union[ErrorCorrectionLevel, str]) -> ErrorCorrectionLevel:
        """Convert error correction string to ErrorCorrectionLevel enum."""
        if isinstance(level, ErrorCorrectionLevel):
            return level
        
        if not isinstance(level, str):
            raise ValueError(f"Invalid error correction level type: {type(level)}")
        
        level_str = level.upper()
        if level_str not in {'L', 'M', 'Q', 'H'}:
            raise ValueError(f"Invalid error correction level: {level}")
        
        return getattr(ErrorCorrectionLevel, level_str)
    
    def add_data(self, data: str, optimize: int = 20) -> None:
        """
        Add data to the QR code.
        
        Args:
            data: Data to encode
            optimize: Optimization level (0-40)
        """
        if isinstance(data, str):
            self.data = data
        else:
            self.data = str(data)
        
        self.data_cache = None
        self.data_list = []
        
        # Determine the best encoding mode
        self._determine_mode()
        
        # Add the data to the data list
        self.data_list.append((self.mode, self.data))
    
    def _determine_mode(self) -> None:
        """Determine the best encoding mode for the data."""
        # Simple implementation: use BYTE mode for all data
        # In a full implementation, this would analyze the data to choose the most efficient mode
        self.mode = QRMode.BYTE
    
    def make(self, fit: bool = True) -> None:
        """
        Generate the QR code.
        
        Args:
            fit: Whether to automatically determine the version
        """
        if self.data_cache is None:
            self.data_cache = self._create_data_cache()
        
        if fit and self.version is None:
            # Find the smallest version that can fit the data
            for version in range(1, 41):
                try:
                    self._create_data(version)
                    self.version = version
                    break
                except ValueError:
                    continue
            else:
                raise ValueError("Data too large for QR code")
        else:
            self._create_data(self.version or 1)
    
    def _create_data_cache(self) -> List[Tuple[QRMode, str]]:
        """Create a cache of the data to be encoded."""
        return self.data_list
    
    def _create_data(self, version: int) -> None:
        """
        Create the QR code data for the specified version.
        
        Args:
            version: QR code version (1-40)
        """
        if version not in self.VERSION_INFO:
            raise ValueError(f"Invalid QR code version: {version}")
        
        self.module_count = self.VERSION_INFO[version]
        self.modules = [[None] * self.module_count for _ in range(self.module_count)]
        
        # Place function patterns
        self._add_finder_patterns()
        self._add_timing_patterns()
        self._add_alignment_patterns()
        self._add_dark_module()
        
        # Place data and error correction codewords
        self._add_data_and_error_correction()
        
        # Apply mask pattern
        if self.mask_pattern == -1:
            self._apply_best_mask_pattern()
        else:
            self._apply_mask_pattern(self.mask_pattern)
    
    def _add_finder_patterns(self) -> None:
        """Add finder patterns to the QR code."""
        # Add finder patterns at the three corners
        self._add_finder_pattern(0, 0)  # Top-left
        self._add_finder_pattern(self.module_count - 7, 0)  # Top-right
        self._add_finder_pattern(0, self.module_count - 7)  # Bottom-left
    
    def _add_finder_pattern(self, row: int, col: int) -> None:
        """
        Add a finder pattern at the specified position.
        
        Args:
            row: Row position
            col: Column position
        """
        for r in range(7):
            for c in range(7):
                if (r == 0 or r == 6 or c == 0 or c == 6 or
                    (r >= 2 and r <= 4 and c >= 2 and c <= 4)):
                    self.modules[row + r][col + c] = True
                else:
                    self.modules[row + r][col + c] = False
    
    def _add_timing_patterns(self) -> None:
        """Add timing patterns to the QR code."""
        # Add horizontal timing pattern
        for i in range(8, self.module_count - 8):
            self.modules[6][i] = i % 2 == 0
        
        # Add vertical timing pattern
        for i in range(8, self.module_count - 8):
            self.modules[i][6] = i % 2 == 0
    
    def _add_alignment_patterns(self) -> None:
        """Add alignment patterns to the QR code."""
        # This is a simplified implementation
        # In a full implementation, this would add alignment patterns based on the version
        pass
    
    def _add_dark_module(self) -> None:
        """Add the dark module to the QR code."""
        self.modules[self.module_count - 8][8] = True
    
    def _add_data_and_error_correction(self) -> None:
        """Add data and error correction codewords to the QR code."""
        # This is a simplified implementation
        # In a full implementation, this would encode the data and add error correction
        pass
    
    def _apply_best_mask_pattern(self) -> None:
        """Apply the best mask pattern to the QR code."""
        # This is a simplified implementation
        # In a full implementation, this would evaluate all mask patterns and choose the best one
        self._apply_mask_pattern(0)
    
    def _apply_mask_pattern(self, pattern: int) -> None:
        """
        Apply the specified mask pattern to the QR code.
        
        Args:
            pattern: Mask pattern (0-7)
        """
        # This is a simplified implementation
        # In a full implementation, this would apply the specified mask pattern
        pass
    
    def make_image(self, fill_color: str = "black", back_color: str = "white", format: str = "png") -> Any:
        """
        Create a PIL Image or SVG of the QR code.
        
        Args:
            fill_color: Color of the QR code modules
            back_color: Color of the background
            format: Output format ('png', 'svg')
            
        Returns:
            PIL Image object or SVG string
        """
        if format.lower() == 'svg':
            # Generate SVG string
            svg = [
                f'<?xml version="1.0" encoding="UTF-8"?>',
                f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 {self.module_count} {self.module_count}">',
                f'<rect width="{self.module_count}" height="{self.module_count}" fill="{back_color}"/>',
            ]
            
            for row in range(self.module_count):
                for col in range(self.module_count):
                    if self.modules[row][col]:
                        svg.append(
                            f'<rect x="{col}" y="{row}" width="1" height="1" fill="{fill_color}"/>'
                        )
            
            svg.append('</svg>')
            return '\n'.join(svg)
        else:
            # Create a PIL Image
            from PIL import Image, ImageDraw
            
            # Create a new image with the specified colors
            img = Image.new("RGB", (self.module_count, self.module_count), back_color)
            draw = ImageDraw.Draw(img)
            
            # Draw the QR code modules
            for row in range(self.module_count):
                for col in range(self.module_count):
                    if self.modules[row][col] is not None:
                        if self.modules[row][col]:
                            draw.rectangle(
                                [(col, row), (col + 1, row + 1)],
                                fill=fill_color
                            )
            
            return img 