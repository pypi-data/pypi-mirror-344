import pytest
from qrcodex.utils import validate_color, validate_size
from qrcodex.exceptions import QRCodeXError

def test_valid_colors():
    """Test valid color formats."""
    # Hex colors
    validate_color("#000000")
    validate_color("#FFFFFF")
    validate_color("#FF0000")
    validate_color("#00FF00")
    validate_color("#0000FF")
    
    # RGB colors
    validate_color("rgb(0, 0, 0)")
    validate_color("rgb(255, 255, 255)")
    validate_color("rgba(255, 0, 0, 0.5)")
    
    # Named colors
    validate_color("black")
    validate_color("white")
    validate_color("red")
    validate_color("blue")

def test_invalid_colors():
    """Test invalid color formats."""
    with pytest.raises(QRCodeXError):
        validate_color("#GGGGGG")
    with pytest.raises(QRCodeXError):
        validate_color("rgb(256, 0, 0)")
    with pytest.raises(QRCodeXError):
        validate_color("not_a_color")

def test_valid_sizes():
    """Test valid size values."""
    assert validate_size(1) == 1
    assert validate_size(10) == 10
    assert validate_size(100) == 100
    assert validate_size(1.0) == 1  # Float should be converted to int

def test_invalid_sizes():
    """Test invalid size values."""
    with pytest.raises(QRCodeXError):
        validate_size(0)
    with pytest.raises(QRCodeXError):
        validate_size(-1)
    with pytest.raises(QRCodeXError):
        validate_size("10")
    with pytest.raises(QRCodeXError):
        validate_size(None) 