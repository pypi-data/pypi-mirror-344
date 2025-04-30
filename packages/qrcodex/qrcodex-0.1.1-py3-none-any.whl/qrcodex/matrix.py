"""
QR Code Matrix Generation and Pattern Placement

This module handles the generation of the QR code matrix and placement of various patterns.
"""

from typing import List, Tuple, Optional
import math

def create_matrix(version: int) -> List[List[Optional[bool]]]:
    """
    Create an empty QR code matrix for the specified version.
    
    Args:
        version: QR code version (1-40)
        
    Returns:
        Empty QR code matrix
    """
    size = (version - 1) * 4 + 21
    return [[None] * size for _ in range(size)]

def add_finder_patterns(matrix: List[List[Optional[bool]]]) -> None:
    """
    Add finder patterns to the QR code matrix.
    
    Args:
        matrix: QR code matrix to modify
    """
    size = len(matrix)
    
    # Add finder patterns at the three corners
    positions = [(0, 0), (size - 7, 0), (0, size - 7)]
    
    for pos in positions:
        row, col = pos
        
        # Outer square
        for i in range(7):
            for j in range(7):
                if i in (0, 6) or j in (0, 6):
                    matrix[row + i][col + j] = True
                else:
                    matrix[row + i][col + j] = False
        
        # Inner square
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    matrix[row + 2 + i][col + 2 + j] = False
                else:
                    matrix[row + 2 + i][col + 2 + j] = True

def add_separator(matrix: List[List[Optional[bool]]]) -> None:
    """
    Add separators between finder patterns.
    
    Args:
        matrix: QR code matrix to modify
    """
    size = len(matrix)
    
    # Add horizontal separator
    for i in range(8):
        matrix[7][i] = False
    
    # Add vertical separator
    for i in range(8):
        matrix[i][7] = False
    
    # Add horizontal separator at bottom left
    for i in range(8):
        matrix[size - 8][i] = False
    
    # Add vertical separator at top right
    for i in range(8):
        matrix[i][size - 8] = False

def add_timing_patterns(matrix: List[List[Optional[bool]]]) -> None:
    """
    Add timing patterns to the QR code matrix.
    
    Args:
        matrix: QR code matrix to modify
    """
    size = len(matrix)
    
    # Add horizontal timing pattern
    for i in range(8, size - 8):
        matrix[6][i] = i % 2 == 0
    
    # Add vertical timing pattern
    for i in range(8, size - 8):
        matrix[i][6] = i % 2 == 0

def add_dark_module(matrix: List[List[Optional[bool]]]) -> None:
    """
    Add the dark module to the QR code matrix.
    
    Args:
        matrix: QR code matrix to modify
    """
    size = len(matrix)
    matrix[size - 8][8] = True

def add_alignment_patterns(matrix: List[List[Optional[bool]]], version: int) -> None:
    """
    Add alignment patterns to the QR code matrix.
    
    Args:
        matrix: QR code matrix to modify
        version: QR code version
    """
    if version == 1:
        return
    
    # Get alignment pattern positions
    positions = get_alignment_positions(version)
    
    for pos in positions:
        row, col = pos
        
        # Skip if position overlaps with finder patterns
        if (row < 9 and col < 9) or (row < 9 and col > size - 9) or (row > size - 9 and col < 9):
            continue
        
        # Add alignment pattern
        for i in range(-2, 3):
            for j in range(-2, 3):
                if abs(i) == 2 or abs(j) == 2:
                    matrix[row + i][col + j] = True
                elif i == 0 and j == 0:
                    matrix[row + i][col + j] = True
                else:
                    matrix[row + i][col + j] = False

def get_alignment_positions(version: int) -> List[Tuple[int, int]]:
    """
    Get the positions for alignment patterns based on version.
    
    Args:
        version: QR code version
        
    Returns:
        List of (row, col) positions for alignment patterns
    """
    if version == 1:
        return []
    
    # Base position for version 2
    positions = [(6, 18), (18, 6), (18, 18)]
    
    if version <= 6:
        return positions
    
    # Add positions for larger versions
    if version <= 13:
        positions.extend([(6, 26), (26, 6), (26, 26)])
    elif version <= 20:
        positions.extend([(6, 34), (34, 6), (34, 34)])
    elif version <= 27:
        positions.extend([(6, 42), (42, 6), (42, 42)])
    elif version <= 34:
        positions.extend([(6, 50), (50, 6), (50, 50)])
    elif version <= 40:
        positions.extend([(6, 58), (58, 6), (58, 58)])
    
    return positions

def add_format_info(matrix: List[List[Optional[bool]]], format_info: List[bool]) -> None:
    """
    Add format information to the QR code matrix.
    
    Args:
        matrix: QR code matrix to modify
        format_info: Format information bits
    """
    size = len(matrix)
    
    # Add format info around the top-left finder pattern
    for i in range(6):
        matrix[8][i] = format_info[i]
    matrix[8][7] = format_info[6]
    matrix[8][8] = format_info[7]
    matrix[7][8] = format_info[8]
    for i in range(6):
        matrix[5 - i][8] = format_info[9 + i]
    
    # Add format info around the top-right and bottom-left finder patterns
    for i in range(8):
        matrix[size - 1 - i][8] = format_info[i]
    for i in range(8):
        matrix[8][size - 1 - i] = format_info[i]

def add_version_info(matrix: List[List[Optional[bool]]], version_info: List[bool]) -> None:
    """
    Add version information to the QR code matrix.
    
    Args:
        matrix: QR code matrix to modify
        version_info: Version information bits
    """
    if len(version_info) == 0:
        return
    
    size = len(matrix)
    
    # Add version info in the bottom-right corner
    for i in range(6):
        for j in range(3):
            matrix[size - 11 + i][j] = version_info[i * 3 + j]
    
    # Add version info in the top-right corner
    for i in range(6):
        for j in range(3):
            matrix[i][size - 11 + j] = version_info[i * 3 + j]

def place_data(matrix: List[List[Optional[bool]]], data: List[bool]) -> None:
    """
    Place the encoded data in the QR code matrix.
    
    Args:
        matrix: QR code matrix to modify
        data: Encoded data bits
    """
    size = len(matrix)
    data_index = 0
    
    # Start from the bottom-right corner and move up in a zigzag pattern
    for col in range(size - 1, -1, -2):
        if col == 6:  # Skip the vertical timing pattern
            col -= 1
        
        for row in range(size - 1, -1, -1):
            # Place two bits in each column
            for i in range(2):
                if col - i < 0:
                    continue
                
                # Skip if the position is already occupied
                if matrix[row][col - i] is not None:
                    continue
                
                # Place the data bit
                if data_index < len(data):
                    matrix[row][col - i] = data[data_index]
                    data_index += 1
                else:
                    matrix[row][col - i] = False  # Fill remaining positions with 0 