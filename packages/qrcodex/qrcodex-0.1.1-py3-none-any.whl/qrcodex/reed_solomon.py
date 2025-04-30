"""
Reed-Solomon Error Correction Implementation

This module implements Reed-Solomon error correction for QR codes.
"""

from typing import List, List, Tuple, Optional
import math

# Galois Field (GF) tables for Reed-Solomon error correction
# These are pre-computed tables for GF(2^8) with primitive polynomial x^8 + x^4 + x^3 + x^2 + 1

# GF(2^8) exponent table
EXP_TABLE = [
    1, 2, 4, 8, 16, 32, 64, 128, 29, 58, 116, 232, 205, 135, 19, 38,
    76, 152, 45, 90, 180, 117, 234, 201, 143, 3, 6, 12, 24, 48, 96, 192,
    157, 39, 78, 156, 37, 74, 148, 53, 106, 212, 181, 119, 238, 193, 159, 35,
    70, 140, 5, 10, 20, 40, 80, 160, 93, 186, 105, 210, 185, 111, 222, 161,
    95, 190, 97, 194, 153, 47, 94, 188, 101, 202, 137, 15, 30, 60, 120, 240,
    253, 231, 211, 187, 107, 214, 177, 127, 254, 225, 223, 163, 91, 182, 113, 226,
    217, 175, 67, 134, 17, 34, 68, 136, 13, 26, 52, 104, 208, 189, 103, 206,
    129, 31, 62, 124, 248, 237, 199, 147, 59, 118, 236, 197, 151, 51, 102, 204,
    133, 23, 46, 92, 184, 109, 218, 169, 79, 158, 33, 66, 132, 21, 42, 84,
    168, 77, 154, 41, 82, 164, 85, 170, 73, 146, 57, 114, 228, 213, 183, 115,
    230, 209, 191, 99, 198, 145, 63, 126, 252, 229, 215, 179, 123, 246, 241, 255,
    227, 219, 171, 75, 150, 49, 98, 196, 149, 55, 110, 220, 165, 87, 174, 65,
    130, 25, 50, 100, 200, 141, 7, 14, 28, 56, 112, 224, 221, 167, 83, 166,
    81, 162, 89, 178, 121, 242, 249, 239, 195, 155, 43, 86, 172, 69, 138, 9,
    18, 36, 72, 144, 61, 122, 244, 245, 247, 243, 251, 235, 203, 139, 11, 22,
    44, 88, 176, 125, 250, 233, 207, 131, 27, 54, 108, 216, 173, 71, 142, 1
]

# GF(2^8) logarithm table
LOG_TABLE = [
    0, 0, 1, 25, 2, 50, 26, 198, 3, 223, 51, 238, 27, 104, 199, 75,
    4, 100, 224, 14, 52, 141, 239, 129, 28, 193, 105, 248, 200, 8, 76, 113,
    5, 138, 101, 47, 225, 36, 15, 33, 53, 147, 142, 218, 240, 18, 130, 69,
    29, 181, 194, 125, 106, 39, 249, 185, 201, 154, 9, 120, 77, 228, 114, 166,
    6, 191, 139, 98, 102, 221, 48, 253, 226, 152, 37, 179, 16, 145, 34, 136,
    54, 208, 148, 206, 143, 150, 219, 189, 241, 210, 19, 92, 131, 56, 70, 64,
    30, 66, 182, 163, 195, 72, 126, 110, 107, 58, 40, 84, 250, 133, 186, 61,
    202, 94, 155, 159, 10, 21, 121, 43, 78, 212, 229, 172, 115, 243, 167, 87,
    7, 112, 192, 247, 140, 128, 99, 13, 103, 74, 222, 237, 49, 197, 254, 24,
    227, 165, 153, 119, 38, 184, 180, 124, 17, 68, 146, 217, 35, 32, 137, 46,
    55, 63, 209, 91, 149, 188, 207, 205, 144, 135, 151, 178, 220, 252, 190, 97,
    242, 86, 211, 171, 20, 42, 93, 158, 132, 60, 57, 83, 71, 109, 65, 162,
    31, 45, 67, 216, 183, 123, 164, 118, 196, 23, 73, 236, 127, 12, 111, 246,
    108, 161, 59, 82, 41, 157, 85, 170, 251, 96, 134, 177, 187, 204, 62, 90,
    203, 89, 95, 176, 156, 169, 160, 81, 11, 245, 22, 235, 122, 117, 44, 215,
    79, 174, 213, 233, 230, 231, 173, 232, 116, 214, 244, 234, 168, 80, 88, 175
]

def gf_multiply(x: int, y: int) -> int:
    """
    Multiply two numbers in GF(2^8).
    
    Args:
        x: First number
        y: Second number
        
    Returns:
        Product in GF(2^8)
    """
    if x == 0 or y == 0:
        return 0
    return EXP_TABLE[(LOG_TABLE[x] + LOG_TABLE[y]) % 255]

def gf_divide(x: int, y: int) -> int:
    """
    Divide two numbers in GF(2^8).
    
    Args:
        x: Numerator
        y: Denominator
        
    Returns:
        Quotient in GF(2^8)
    """
    if y == 0:
        raise ZeroDivisionError("Division by zero in GF(2^8)")
    if x == 0:
        return 0
    return EXP_TABLE[(LOG_TABLE[x] - LOG_TABLE[y]) % 255]

def gf_poly_multiply(p1: List[int], p2: List[int]) -> List[int]:
    """
    Multiply two polynomials in GF(2^8).
    
    Args:
        p1: First polynomial coefficients
        p2: Second polynomial coefficients
        
    Returns:
        Product polynomial coefficients
    """
    result = [0] * (len(p1) + len(p2) - 1)
    for i in range(len(p1)):
        for j in range(len(p2)):
            result[i + j] ^= gf_multiply(p1[i], p2[j])
    return result

def gf_poly_divide(dividend: List[int], divisor: List[int]) -> Tuple[List[int], List[int]]:
    """
    Divide two polynomials in GF(2^8).
    
    Args:
        dividend: Dividend polynomial coefficients
        divisor: Divisor polynomial coefficients
        
    Returns:
        Tuple of (quotient, remainder) polynomial coefficients
    """
    if len(divisor) == 0:
        raise ValueError("Divisor polynomial is empty")
    
    if len(dividend) < len(divisor):
        return [], dividend
    
    result = [0] * (len(dividend) - len(divisor) + 1)
    remainder = dividend.copy()
    
    for i in range(len(dividend) - len(divisor) + 1):
        if remainder[i] != 0:
            coef = gf_divide(remainder[i], divisor[0])
            result[i] = coef
            
            for j in range(len(divisor)):
                remainder[i + j] ^= gf_multiply(coef, divisor[j])
    
    return result, remainder[-(len(divisor) - 1):]

def rs_generator_poly(nsym: int) -> List[int]:
    """
    Generate the Reed-Solomon generator polynomial.
    
    Args:
        nsym: Number of error correction symbols
        
    Returns:
        Generator polynomial coefficients
    """
    g = [1]
    for i in range(nsym):
        g = gf_poly_multiply(g, [1, EXP_TABLE[i]])
    return g

def rs_encode_msg(msg_in: List[int], nsym: int) -> List[int]:
    """
    Encode a message with Reed-Solomon error correction.
    
    Args:
        msg_in: Message to encode
        nsym: Number of error correction symbols
        
    Returns:
        Encoded message with error correction symbols
    """
    if len(msg_in) + nsym > 255:
        raise ValueError("Message too long for Reed-Solomon encoding")
    
    # Generate the generator polynomial
    g = rs_generator_poly(nsym)
    
    # Pad the message with zeros
    msg_out = msg_in + [0] * nsym
    
    # Perform polynomial division
    for i in range(len(msg_in)):
        if msg_out[i] != 0:
            for j in range(len(g)):
                msg_out[i + j] ^= gf_multiply(g[j], msg_out[i])
    
    # Replace the padding with the remainder
    for i in range(nsym):
        msg_out[len(msg_in) + i] = msg_out[i]
    
    return msg_out[len(msg_in):]

def rs_correct_msg(msg_in: List[int], nsym: int) -> Tuple[List[int], List[int], bool]:
    """
    Correct errors in a Reed-Solomon encoded message.
    
    Args:
        msg_in: Message to correct
        nsym: Number of error correction symbols
        
    Returns:
        Tuple of (corrected message, error locations, success)
    """
    if len(msg_in) > 255:
        raise ValueError("Message too long for Reed-Solomon decoding")
    
    # Calculate syndromes
    syndromes = [0] * nsym
    for i in range(nsym):
        for j in range(len(msg_in)):
            syndromes[i] ^= gf_multiply(msg_in[j], EXP_TABLE[i * j])
    
    # Check if there are errors
    if all(s == 0 for s in syndromes):
        return msg_in, [], True
    
    # Find error locator polynomial using Berlekamp-Massey algorithm
    err_loc = [1]
    old_loc = [1]
    for i in range(nsym):
        delta = syndromes[i]
        for j in range(1, len(err_loc)):
            delta ^= gf_multiply(err_loc[-(j + 1)], syndromes[i - j])
        
        if delta != 0:
            if len(old_loc) > len(err_loc):
                new_loc = old_loc + [0] * (len(err_loc) - len(old_loc))
                for j in range(len(err_loc)):
                    new_loc[j] = err_loc[j] ^ gf_multiply(delta, new_loc[j])
                err_loc = new_loc
            else:
                new_loc = err_loc.copy()
                for j in range(len(old_loc)):
                    new_loc[j] = err_loc[j] ^ gf_multiply(delta, old_loc[j])
                err_loc = new_loc
            old_loc = [x for x in err_loc]
    
    # Find error locations using Chien search
    err_pos = []
    for i in range(255):
        x = 0
        for j in range(len(err_loc)):
            x ^= gf_multiply(err_loc[j], EXP_TABLE[(i * j) % 255])
        if x == 0:
            err_pos.append(255 - i)
    
    # Find error values using Forney algorithm
    err_val = [0] * len(err_pos)
    for i in range(len(err_pos)):
        x = EXP_TABLE[err_pos[i]]
        omega = 0
        for j in range(nsym):
            omega ^= gf_multiply(syndromes[j], EXP_TABLE[(j * (255 - err_pos[i])) % 255])
        
        err_loc_prime = 0
        for j in range(len(err_loc)):
            if j % 2 == 1:
                err_loc_prime ^= gf_multiply(err_loc[j], EXP_TABLE[(j * (255 - err_pos[i])) % 255])
        
        err_val[i] = gf_divide(omega, err_loc_prime)
    
    # Correct the errors
    msg_out = msg_in.copy()
    for i in range(len(err_pos)):
        msg_out[err_pos[i]] ^= err_val[i]
    
    return msg_out, err_pos, True 