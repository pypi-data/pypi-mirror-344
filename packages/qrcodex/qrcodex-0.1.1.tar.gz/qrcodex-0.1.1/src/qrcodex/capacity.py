"""
QR Code Version and Capacity Information

This module provides information about QR code versions, capacities, and error correction levels.
"""

from enum import Enum
from typing import Dict, List, Tuple

class ErrorCorrectionLevel(Enum):
    """Error correction levels for QR codes."""
    L = 0  # 7% recovery capacity
    M = 1  # 15% recovery capacity
    Q = 2  # 25% recovery capacity
    H = 3  # 30% recovery capacity

# Capacity information for each version and error correction level
# Format: (version, error_correction_level) -> (numeric_capacity, alphanumeric_capacity, byte_capacity, kanji_capacity)
CAPACITY_INFO: Dict[Tuple[int, ErrorCorrectionLevel], Tuple[int, int, int, int]] = {
    (1, ErrorCorrectionLevel.L): (41, 25, 17, 10),
    (1, ErrorCorrectionLevel.M): (34, 20, 14, 8),
    (1, ErrorCorrectionLevel.Q): (27, 16, 11, 7),
    (1, ErrorCorrectionLevel.H): (17, 10, 7, 4),
    (2, ErrorCorrectionLevel.L): (77, 47, 32, 20),
    (2, ErrorCorrectionLevel.M): (63, 38, 26, 16),
    (2, ErrorCorrectionLevel.Q): (48, 29, 20, 12),
    (2, ErrorCorrectionLevel.H): (34, 20, 14, 8),
    (3, ErrorCorrectionLevel.L): (127, 77, 53, 32),
    (3, ErrorCorrectionLevel.M): (101, 61, 42, 26),
    (3, ErrorCorrectionLevel.Q): (77, 47, 32, 20),
    (3, ErrorCorrectionLevel.H): (58, 35, 24, 15),
    (4, ErrorCorrectionLevel.L): (187, 114, 78, 48),
    (4, ErrorCorrectionLevel.M): (149, 90, 62, 38),
    (4, ErrorCorrectionLevel.Q): (111, 67, 46, 28),
    (4, ErrorCorrectionLevel.H): (82, 50, 34, 21),
    (5, ErrorCorrectionLevel.L): (255, 154, 106, 65),
    (5, ErrorCorrectionLevel.M): (202, 122, 84, 52),
    (5, ErrorCorrectionLevel.Q): (144, 87, 60, 37),
    (5, ErrorCorrectionLevel.H): (106, 64, 44, 27),
    (6, ErrorCorrectionLevel.L): (322, 195, 134, 82),
    (6, ErrorCorrectionLevel.M): (255, 154, 106, 65),
    (6, ErrorCorrectionLevel.Q): (178, 108, 74, 45),
    (6, ErrorCorrectionLevel.H): (139, 84, 58, 36),
    (7, ErrorCorrectionLevel.L): (370, 224, 154, 95),
    (7, ErrorCorrectionLevel.M): (293, 178, 122, 75),
    (7, ErrorCorrectionLevel.Q): (207, 125, 86, 53),
    (7, ErrorCorrectionLevel.H): (154, 93, 64, 39),
    (8, ErrorCorrectionLevel.L): (461, 279, 192, 118),
    (8, ErrorCorrectionLevel.M): (365, 221, 152, 93),
    (8, ErrorCorrectionLevel.Q): (259, 157, 108, 66),
    (8, ErrorCorrectionLevel.H): (202, 122, 84, 52),
    (9, ErrorCorrectionLevel.L): (552, 335, 230, 141),
    (9, ErrorCorrectionLevel.M): (432, 262, 180, 111),
    (9, ErrorCorrectionLevel.Q): (312, 189, 130, 80),
    (9, ErrorCorrectionLevel.H): (235, 143, 98, 60),
    (10, ErrorCorrectionLevel.L): (652, 395, 271, 167),
    (10, ErrorCorrectionLevel.M): (513, 311, 213, 131),
    (10, ErrorCorrectionLevel.Q): (364, 221, 151, 93),
    (10, ErrorCorrectionLevel.H): (288, 174, 119, 74),
}

# Number of error correction codewords per block
ERROR_CORRECTION_CODEWORDS: Dict[Tuple[int, ErrorCorrectionLevel], int] = {
    (1, ErrorCorrectionLevel.L): 7,
    (1, ErrorCorrectionLevel.M): 10,
    (1, ErrorCorrectionLevel.Q): 13,
    (1, ErrorCorrectionLevel.H): 17,
    (2, ErrorCorrectionLevel.L): 10,
    (2, ErrorCorrectionLevel.M): 16,
    (2, ErrorCorrectionLevel.Q): 22,
    (2, ErrorCorrectionLevel.H): 28,
    # Add more versions as needed
}

# Number of blocks and codewords per block
BLOCK_INFO: Dict[Tuple[int, ErrorCorrectionLevel], List[Tuple[int, int]]] = {
    (1, ErrorCorrectionLevel.L): [(1, 19)],
    (1, ErrorCorrectionLevel.M): [(1, 16)],
    (1, ErrorCorrectionLevel.Q): [(1, 13)],
    (1, ErrorCorrectionLevel.H): [(1, 9)],
    (2, ErrorCorrectionLevel.L): [(1, 34)],
    (2, ErrorCorrectionLevel.M): [(1, 28)],
    (2, ErrorCorrectionLevel.Q): [(1, 22)],
    (2, ErrorCorrectionLevel.H): [(1, 16)],
    # Add more versions as needed
}

def get_capacity(version: int, error_correction_level: ErrorCorrectionLevel, mode: str) -> int:
    """
    Get the capacity for a specific version, error correction level, and mode.
    
    Args:
        version: QR code version (1-40)
        error_correction_level: Error correction level
        mode: Encoding mode ('numeric', 'alphanumeric', 'byte', 'kanji')
        
    Returns:
        Number of characters that can be encoded
    """
    if (version, error_correction_level) not in CAPACITY_INFO:
        raise ValueError(f"Invalid version {version} or error correction level {error_correction_level}")
    
    capacities = CAPACITY_INFO[(version, error_correction_level)]
    mode_index = {'numeric': 0, 'alphanumeric': 1, 'byte': 2, 'kanji': 3}[mode.lower()]
    return capacities[mode_index]

def get_error_correction_codewords(version: int, error_correction_level: ErrorCorrectionLevel) -> int:
    """
    Get the number of error correction codewords for a specific version and error correction level.
    
    Args:
        version: QR code version (1-40)
        error_correction_level: Error correction level
        
    Returns:
        Number of error correction codewords
    """
    if (version, error_correction_level) not in ERROR_CORRECTION_CODEWORDS:
        raise ValueError(f"Invalid version {version} or error correction level {error_correction_level}")
    
    return ERROR_CORRECTION_CODEWORDS[(version, error_correction_level)]

def get_block_info(version: int, error_correction_level: ErrorCorrectionLevel) -> List[Tuple[int, int]]:
    """
    Get the block information for a specific version and error correction level.
    
    Args:
        version: QR code version (1-40)
        error_correction_level: Error correction level
        
    Returns:
        List of tuples (number of blocks, codewords per block)
    """
    if (version, error_correction_level) not in BLOCK_INFO:
        raise ValueError(f"Invalid version {version} or error correction level {error_correction_level}")
    
    return BLOCK_INFO[(version, error_correction_level)]

def get_minimum_version(data_length: int, mode: str, error_correction_level: ErrorCorrectionLevel) -> int:
    """
    Find the minimum version that can encode the given data length.
    
    Args:
        data_length: Length of the data to encode
        mode: Encoding mode ('numeric', 'alphanumeric', 'byte', 'kanji')
        error_correction_level: Error correction level
        
    Returns:
        Minimum version number that can encode the data
    """
    for version in range(1, 41):
        try:
            capacity = get_capacity(version, error_correction_level, mode)
            if capacity >= data_length:
                return version
        except ValueError:
            continue
    
    raise ValueError("Data too long for QR code") 