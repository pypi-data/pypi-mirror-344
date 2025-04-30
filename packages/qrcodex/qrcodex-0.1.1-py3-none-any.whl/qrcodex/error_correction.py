"""
QR Code Error Correction Coding

This module implements Reed-Solomon error correction coding for QR codes.
"""

from typing import List, Tuple
import math

# Generator polynomial coefficients for different error correction levels
GENERATOR_POLYNOMIALS = {
    7: [1, 127, 122, 154, 164, 11, 68, 117],
    10: [1, 216, 194, 159, 111, 199, 94, 95, 113, 157, 193],
    13: [1, 137, 73, 227, 17, 177, 17, 52, 13, 46, 43, 83, 132, 120],
    15: [1, 29, 196, 111, 163, 112, 74, 10, 105, 105, 139, 132, 151, 32, 134, 26],
    16: [1, 59, 13, 104, 189, 175, 31, 97, 17, 79, 32, 185, 8, 7, 187, 62, 8],
    17: [1, 119, 66, 83, 120, 119, 49, 60, 202, 80, 171, 21, 122, 149, 169, 25, 133, 142],
    18: [1, 239, 251, 183, 113, 149, 175, 199, 215, 240, 220, 73, 82, 173, 75, 32, 67, 217, 146],
    20: [1, 152, 185, 240, 5, 111, 99, 6, 220, 112, 150, 69, 36, 187, 22, 228, 198, 121, 121, 165, 174],
    22: [1, 89, 179, 131, 96, 24, 231, 101, 215, 14, 57, 42, 242, 97, 6, 199, 39, 235, 55, 3, 244, 55, 3],
    24: [1, 173, 125, 158, 2, 103, 182, 118, 17, 145, 201, 111, 28, 165, 53, 161, 21, 245, 142, 13, 102, 48, 227, 153, 145],
    26: [1, 168, 223, 200, 104, 224, 234, 108, 180, 110, 190, 195, 147, 205, 27, 232, 201, 21, 43, 245, 87, 42, 195, 212, 119, 242, 37, 9, 123],
    28: [1, 41, 173, 145, 152, 216, 31, 179, 182, 50, 48, 110, 86, 239, 96, 222, 125, 42, 173, 46, 221, 43, 96, 253, 242, 24, 152, 7, 238, 37, 132, 86],
    30: [1, 10, 251, 167, 48, 171, 61, 10, 83, 23, 65, 29, 14, 167, 229, 73, 67, 58, 254, 34, 8, 6, 90, 185, 175, 229, 24, 5, 243, 111, 7, 158, 13, 131, 11, 110, 67]
}

def gf_multiply(a: int, b: int) -> int:
    """
    Multiply two numbers in GF(256).
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Product in GF(256)
    """
    if a == 0 or b == 0:
        return 0
    
    return GF_EXP[(GF_LOG[a] + GF_LOG[b]) % 255]

def gf_divide(a: int, b: int) -> int:
    """
    Divide two numbers in GF(256).
    
    Args:
        a: Dividend
        b: Divisor
        
    Returns:
        Quotient in GF(256)
    """
    if b == 0:
        raise ValueError("Division by zero")
    if a == 0:
        return 0
    
    return GF_EXP[(GF_LOG[a] - GF_LOG[b] + 255) % 255]

def create_generator_polynomial(degree: int) -> List[int]:
    """
    Create a generator polynomial of the specified degree.
    
    Args:
        degree: Degree of the generator polynomial
        
    Returns:
        List of coefficients of the generator polynomial
    """
    if degree in GENERATOR_POLYNOMIALS:
        return GENERATOR_POLYNOMIALS[degree]
    
    # Start with (x - α^0)
    poly = [1, 1]
    
    # Multiply by (x - α^i) for i = 1 to degree-1
    for i in range(1, degree):
        # Multiply current polynomial by (x - α^i)
        new_poly = [0] * (len(poly) + 1)
        for j in range(len(poly)):
            new_poly[j] = poly[j]
            if j > 0:
                new_poly[j] ^= gf_multiply(poly[j-1], GF_EXP[i])
        poly = new_poly
    
    return poly

def encode_blocks(data: List[int], num_error_correction_codewords: int) -> List[int]:
    """
    Encode data blocks using Reed-Solomon error correction.
    
    Args:
        data: List of data codewords
        num_error_correction_codewords: Number of error correction codewords
        
    Returns:
        List of error correction codewords
    """
    # Create generator polynomial
    generator = create_generator_polynomial(num_error_correction_codewords)
    
    # Initialize message polynomial with data codewords
    message = [0] * (len(data) + num_error_correction_codewords)
    for i in range(len(data)):
        message[i] = data[i]
    
    # Perform polynomial division
    for i in range(len(data)):
        if message[i] == 0:
            continue
        
        # Multiply generator by the current coefficient
        factor = message[i]
        for j in range(len(generator)):
            message[i + j] ^= gf_multiply(generator[j], factor)
    
    # Return error correction codewords
    return message[len(data):]

def decode_blocks(data: List[int], num_error_correction_codewords: int) -> Tuple[List[int], List[int]]:
    """
    Decode data blocks and correct errors using Reed-Solomon error correction.
    
    Args:
        data: List of received codewords
        num_error_correction_codewords: Number of error correction codewords
        
    Returns:
        Tuple of (corrected data, error locations)
    """
    # Calculate syndromes
    syndromes = [0] * num_error_correction_codewords
    for i in range(num_error_correction_codewords):
        for j in range(len(data)):
            syndromes[i] ^= gf_multiply(data[j], GF_EXP[i * j])
    
    # Check if there are errors
    if all(s == 0 for s in syndromes):
        return data[:-num_error_correction_codewords], []
    
    # Find error locator polynomial using Berlekamp-Massey algorithm
    error_locator = [1]
    old_locator = [1]
    for i in range(num_error_correction_codewords):
        # Calculate discrepancy
        delta = syndromes[i]
        for j in range(1, len(error_locator)):
            delta ^= gf_multiply(error_locator[j], syndromes[i - j])
        
        if delta != 0:
            if len(old_locator) > len(error_locator):
                # Adjust error locator polynomial
                new_locator = [0] * len(old_locator)
                for j in range(len(error_locator)):
                    new_locator[j] = error_locator[j]
                for j in range(len(old_locator) - len(error_locator)):
                    new_locator[j + len(error_locator)] = gf_multiply(old_locator[j + len(error_locator)], delta)
                error_locator = new_locator
            else:
                # Shift and add
                temp = [0] * (len(error_locator) + 1)
                for j in range(len(error_locator)):
                    temp[j] = error_locator[j]
                for j in range(len(old_locator)):
                    temp[j + 1] ^= gf_multiply(old_locator[j], delta)
                error_locator = temp
        
        old_locator = error_locator[:]
    
    # Find error locations using Chien search
    error_locations = []
    for i in range(len(data)):
        sum = 0
        for j in range(len(error_locator)):
            sum ^= gf_multiply(error_locator[j], GF_EXP[(j * i) % 255])
        if sum == 0:
            error_locations.append(len(data) - 1 - i)
    
    # Correct errors using Forney algorithm
    corrected_data = data[:]
    for pos in error_locations:
        # Calculate error magnitude
        x = GF_EXP[pos]
        omega = 0
        for i in range(len(syndromes)):
            omega ^= gf_multiply(syndromes[i], GF_EXP[i * pos])
        
        # Calculate error locator polynomial derivative
        deriv = 0
        for i in range(1, len(error_locator), 2):
            deriv ^= error_locator[i]
        
        # Calculate error value
        error_value = gf_divide(omega, deriv)
        
        # Correct the error
        corrected_data[pos] ^= error_value
    
    return corrected_data[:-num_error_correction_codewords], error_locations

# Initialize Galois Field tables
GF_EXP = [0] * 256
GF_LOG = [0] * 256

# Generate Galois Field tables
x = 1
for i in range(255):
    GF_EXP[i] = x
    GF_LOG[x] = i
    x = (x * 2) ^ (0x11D if x & 0x80 else 0)
GF_EXP[255] = 1 