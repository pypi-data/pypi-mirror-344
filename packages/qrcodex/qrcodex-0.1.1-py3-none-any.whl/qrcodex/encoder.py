"""
QR Code Data Encoding and Masking

This module implements the data encoding and masking algorithms for QR codes.
"""

from typing import List, List, Tuple, Optional
from enum import Enum
import math

class QRMode(Enum):
    """QR Code encoding modes."""
    NUMERIC = 1
    ALPHANUMERIC = 2
    BYTE = 4
    KANJI = 8

class ErrorCorrectionLevel(Enum):
    """QR Code error correction levels."""
    L = 1  # 7% recovery capacity
    M = 0  # 15% recovery capacity
    Q = 3  # 25% recovery capacity
    H = 2  # 30% recovery capacity

# Character count indicator bits
CHAR_COUNT_BITS = {
    QRMode.NUMERIC: {1: 10, 2: 12, 3: 14},
    QRMode.ALPHANUMERIC: {1: 9, 2: 11, 3: 13},
    QRMode.BYTE: {1: 8, 2: 16, 3: 16},
    QRMode.KANJI: {1: 8, 2: 10, 3: 12}
}

# Alphanumeric character encoding table
ALPHANUMERIC_TABLE = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18,
    'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27,
    'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35,
    ' ': 36, '$': 37, '%': 38, '*': 39, '+': 40, '-': 41, '.': 42, '/': 43, ':': 44
}

def encode_numeric(data: str) -> List[int]:
    """
    Encode numeric data into QR code format.
    
    Args:
        data: Numeric string to encode
        
    Returns:
        List of encoded bytes
    """
    result = []
    for i in range(0, len(data), 3):
        chunk = data[i:i + 3]
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
    Encode alphanumeric data into QR code format.
    
    Args:
        data: Alphanumeric string to encode
        
    Returns:
        List of encoded bytes
    """
    result = []
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            value = ALPHANUMERIC_TABLE[data[i]] * 45 + ALPHANUMERIC_TABLE[data[i + 1]]
            result.append(value)
        else:
            value = ALPHANUMERIC_TABLE[data[i]]
            result.append(value)
    return result

def encode_byte(data: str) -> List[int]:
    """
    Encode byte data into QR code format.
    
    Args:
        data: String to encode as bytes
        
    Returns:
        List of encoded bytes
    """
    return [ord(c) for c in data]

def encode_kanji(data: str) -> List[int]:
    """
    Encode Kanji data into QR code format.
    
    Args:
        data: Kanji string to encode
        
    Returns:
        List of encoded bytes
    """
    result = []
    for c in data:
        # Convert character to Shift-JIS encoding
        sjis = ord(c)
        if 0x8140 <= sjis <= 0x9FFC:
            sjis -= 0x8140
        elif 0xE040 <= sjis <= 0xEBBF:
            sjis -= 0xC140
        else:
            raise ValueError(f"Invalid Kanji character: {c}")
        
        # Encode as 13-bit value
        msb = (sjis >> 8) & 0xFF
        lsb = sjis & 0xFF
        value = (msb * 0xC0) + lsb
        result.extend([value >> 8, value & 0xFF])
    return result

def get_mode_indicator(mode: QRMode) -> int:
    """
    Get the mode indicator bits for a QR code mode.
    
    Args:
        mode: QR code mode
        
    Returns:
        Mode indicator bits
    """
    return mode.value

def get_char_count_indicator(data: str, mode: QRMode, version: int) -> List[int]:
    """
    Get the character count indicator bits.
    
    Args:
        data: Data to encode
        mode: QR code mode
        version: QR code version
        
    Returns:
        Character count indicator bits
    """
    # Determine version range
    if version <= 9:
        version_range = 1
    elif version <= 26:
        version_range = 2
    else:
        version_range = 3
    
    # Get number of bits
    bits = CHAR_COUNT_BITS[mode][version_range]
    
    # Convert length to binary
    length = len(data)
    result = []
    for _ in range(bits):
        result.insert(0, length & 1)
        length >>= 1
    return result

def apply_mask_pattern(data: List[List[bool]], pattern: int) -> List[List[bool]]:
    """
    Apply a mask pattern to the QR code data.
    
    Args:
        data: QR code data matrix
        pattern: Mask pattern number (0-7)
        
    Returns:
        Masked QR code data matrix
    """
    size = len(data)
    result = [[False] * size for _ in range(size)]
    
    for i in range(size):
        for j in range(size):
            if data[i][j]:
                if pattern == 0 and (i + j) % 2 == 0:
                    result[i][j] = True
                elif pattern == 1 and i % 2 == 0:
                    result[i][j] = True
                elif pattern == 2 and j % 3 == 0:
                    result[i][j] = True
                elif pattern == 3 and (i + j) % 3 == 0:
                    result[i][j] = True
                elif pattern == 4 and (i // 2 + j // 3) % 2 == 0:
                    result[i][j] = True
                elif pattern == 5 and (i * j) % 2 + (i * j) % 3 == 0:
                    result[i][j] = True
                elif pattern == 6 and ((i * j) % 2 + (i * j) % 3) % 2 == 0:
                    result[i][j] = True
                elif pattern == 7 and ((i * j) % 3 + (i + j) % 2) % 2 == 0:
                    result[i][j] = True
                else:
                    result[i][j] = False
            else:
                result[i][j] = data[i][j]
    
    return result

def calculate_mask_penalty(data: List[List[bool]]) -> int:
    """
    Calculate the penalty score for a mask pattern.
    
    Args:
        data: QR code data matrix
        
    Returns:
        Penalty score
    """
    size = len(data)
    penalty = 0
    
    # Rule 1: Penalty for each group of 5 or more consecutive modules of the same color
    for i in range(size):
        count = 1
        last = data[i][0]
        for j in range(1, size):
            if data[i][j] == last:
                count += 1
                if count >= 5:
                    penalty += count - 2
            else:
                count = 1
                last = data[i][j]
    
    for j in range(size):
        count = 1
        last = data[0][j]
        for i in range(1, size):
            if data[i][j] == last:
                count += 1
                if count >= 5:
                    penalty += count - 2
            else:
                count = 1
                last = data[i][j]
    
    # Rule 2: Penalty for each 2x2 block of modules of the same color
    for i in range(size - 1):
        for j in range(size - 1):
            if (data[i][j] == data[i + 1][j] == data[i][j + 1] == data[i + 1][j + 1]):
                penalty += 3
    
    # Rule 3: Penalty for patterns similar to the finder pattern
    pattern1 = [True, False, True, True, True, False, True]
    pattern2 = [True, True, True, False, True]
    
    for i in range(size - 6):
        for j in range(size - 6):
            # Check horizontal pattern
            match = True
            for k in range(7):
                if data[i][j + k] != pattern1[k]:
                    match = False
                    break
            if match:
                penalty += 40
            
            # Check vertical pattern
            match = True
            for k in range(7):
                if data[i + k][j] != pattern1[k]:
                    match = False
                    break
            if match:
                penalty += 40
    
    for i in range(size - 4):
        for j in range(size - 4):
            # Check horizontal pattern
            match = True
            for k in range(5):
                if data[i][j + k] != pattern2[k]:
                    match = False
                    break
            if match:
                penalty += 40
            
            # Check vertical pattern
            match = True
            for k in range(5):
                if data[i + k][j] != pattern2[k]:
                    match = False
                    break
            if match:
                penalty += 40
    
    # Rule 4: Penalty for unbalanced proportion of dark and light modules
    dark_count = sum(sum(row) for row in data)
    total = size * size
    percentage = dark_count * 100 // total
    
    # Calculate penalty based on how far the percentage is from 50%
    penalty += min(abs(percentage - 50) // 5, 10) * 10
    
    return penalty

def find_best_mask_pattern(data: List[List[bool]]) -> Tuple[int, List[List[bool]]]:
    """
    Find the best mask pattern for the QR code data.
    
    Args:
        data: QR code data matrix
        
    Returns:
        Tuple of (best pattern number, masked data)
    """
    best_pattern = 0
    best_penalty = float('inf')
    best_data = None
    
    for pattern in range(8):
        masked_data = apply_mask_pattern(data, pattern)
        penalty = calculate_mask_penalty(masked_data)
        
        if penalty < best_penalty:
            best_pattern = pattern
            best_penalty = penalty
            best_data = masked_data
    
    return best_pattern, best_data 