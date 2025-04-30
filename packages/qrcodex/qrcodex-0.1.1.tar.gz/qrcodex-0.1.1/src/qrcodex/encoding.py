"""
QR Code Data Encoding

This module handles the encoding of data into QR code format, including mode selection,
character count indicators, and data encoding for different modes.
"""

from typing import List, Tuple, Union
import re
from .capacity import ErrorCorrectionLevel

class EncodingMode:
    """Encoding modes for QR codes."""
    NUMERIC = 'numeric'
    ALPHANUMERIC = 'alphanumeric'
    BYTE = 'byte'
    KANJI = 'kanji'

# Mode indicator bits
MODE_INDICATORS = {
    EncodingMode.NUMERIC: 0b0001,
    EncodingMode.ALPHANUMERIC: 0b0010,
    EncodingMode.BYTE: 0b0100,
    EncodingMode.KANJI: 0b1000,
}

# Character count indicator bits length
CHARACTER_COUNT_BITS = {
    1: {EncodingMode.NUMERIC: 10, EncodingMode.ALPHANUMERIC: 9, EncodingMode.BYTE: 8, EncodingMode.KANJI: 8},
    2: {EncodingMode.NUMERIC: 12, EncodingMode.ALPHANUMERIC: 11, EncodingMode.BYTE: 16, EncodingMode.KANJI: 10},
    3: {EncodingMode.NUMERIC: 14, EncodingMode.ALPHANUMERIC: 13, EncodingMode.BYTE: 16, EncodingMode.KANJI: 12},
}

# Alphanumeric encoding table
ALPHANUMERIC_TABLE = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18,
    'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27,
    'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35,
    ' ': 36, '$': 37, '%': 38, '*': 39, '+': 40, '-': 41, '.': 42, '/': 43, ':': 44,
}

def select_mode(data: str) -> str:
    """
    Select the most efficient encoding mode for the given data.
    
    Args:
        data: The data to encode
        
    Returns:
        Selected encoding mode
    """
    if re.match(r'^[0-9]*$', data):
        return EncodingMode.NUMERIC
    elif re.match(r'^[0-9A-Z $%*+\-./:]*$', data):
        return EncodingMode.ALPHANUMERIC
    else:
        return EncodingMode.BYTE

def encode_numeric(data: str) -> List[int]:
    """
    Encode numeric data.
    
    Args:
        data: Numeric string to encode
        
    Returns:
        List of encoded bytes
    """
    result = []
    for i in range(0, len(data), 3):
        chunk = data[i:i+3]
        if len(chunk) == 3:
            value = int(chunk)
            result.extend([value >> 8, value & 0xFF])
        elif len(chunk) == 2:
            value = int(chunk)
            result.append(value)
        else:
            value = int(chunk)
            result.append(value)
    return result

def encode_alphanumeric(data: str) -> List[int]:
    """
    Encode alphanumeric data.
    
    Args:
        data: Alphanumeric string to encode
        
    Returns:
        List of encoded bytes
    """
    result = []
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            value = ALPHANUMERIC_TABLE[data[i]] * 45 + ALPHANUMERIC_TABLE[data[i+1]]
            result.append(value)
        else:
            value = ALPHANUMERIC_TABLE[data[i]]
            result.append(value)
    return result

def encode_byte(data: str) -> List[int]:
    """
    Encode byte data.
    
    Args:
        data: String to encode as bytes
        
    Returns:
        List of encoded bytes
    """
    return [ord(c) for c in data]

def encode_data(data: str, version: int, error_correction_level: ErrorCorrectionLevel) -> List[int]:
    """
    Encode data into QR code format.
    
    Args:
        data: Data to encode
        version: QR code version
        error_correction_level: Error correction level
        
    Returns:
        List of encoded bytes
    """
    # Select encoding mode
    mode = select_mode(data)
    
    # Get character count indicator bits length
    if version <= 9:
        version_range = 1
    elif version <= 26:
        version_range = 2
    else:
        version_range = 3
    
    char_count_bits = CHARACTER_COUNT_BITS[version_range][mode]
    
    # Encode mode indicator
    result = [MODE_INDICATORS[mode]]
    
    # Encode character count indicator
    char_count = len(data)
    result.extend([(char_count >> (i * 8)) & 0xFF for i in range(char_count_bits // 8)])
    
    # Encode data
    if mode == EncodingMode.NUMERIC:
        result.extend(encode_numeric(data))
    elif mode == EncodingMode.ALPHANUMERIC:
        result.extend(encode_alphanumeric(data))
    else:
        result.extend(encode_byte(data))
    
    return result

def add_padding(data: List[int], version: int, error_correction_level: ErrorCorrectionLevel) -> List[int]:
    """
    Add padding bits to complete the data codewords.
    
    Args:
        data: Encoded data
        version: QR code version
        error_correction_level: Error correction level
        
    Returns:
        Padded data
    """
    # Calculate required number of codewords
    total_codewords = version * 4 + 17  # Simplified calculation
    data_codewords = total_codewords - error_correction_level.value * 4
    
    # Add terminator
    terminator_bits = min(4, (data_codewords * 8) - len(data) * 8)
    data.extend([0] * (terminator_bits // 8))
    
    # Add padding bytes
    while len(data) < data_codewords:
        data.extend([0xEC, 0x11][len(data) % 2])
    
    return data 