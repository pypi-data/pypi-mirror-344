"""Test cases for QR code generator."""

import pytest
from pathlib import Path
from PIL import Image
import base64
from io import BytesIO

from qrcodex import QRCodeX, QRCodeXError

def test_basic_qr_generation(tmp_path):
    """Test basic QR code generation."""
    output = tmp_path / "test.png"
    qr = QRCodeX()
    qr.add_data("Hello, World!")
    qr.generate(output)
    assert output.exists()
    assert output.stat().st_size > 0

def test_invalid_error_correction():
    """Test invalid error correction level."""
    with pytest.raises(QRCodeXError):
        QRCodeX(error_correction="X")

def test_invalid_box_size():
    """Test invalid box size."""
    with pytest.raises(QRCodeXError):
        QRCodeX(box_size=0)

def test_invalid_border():
    """Test invalid border size."""
    with pytest.raises(QRCodeXError):
        QRCodeX(border=-1)

def test_invalid_version():
    """Test invalid version number."""
    with pytest.raises(QRCodeXError):
        QRCodeX(version=0)
    with pytest.raises(QRCodeXError):
        QRCodeX(version=41)

def test_empty_data():
    """Test empty data handling."""
    qr = QRCodeX()
    with pytest.raises(QRCodeXError):
        qr.generate("test.png")

def test_none_data():
    """Test None data handling."""
    qr = QRCodeX()
    with pytest.raises(QRCodeXError):
        qr.add_data(None)

def test_invalid_data_type():
    """Test invalid data type handling."""
    qr = QRCodeX()
    with pytest.raises(QRCodeXError):
        qr.add_data("test", data_type="invalid")

def test_binary_data():
    """Test binary data handling."""
    qr = QRCodeX()
    data = bytes([0x00, 0xFF, 0xAA, 0x55])
    qr.add_data(data, data_type="binary")
    assert len(qr.data_list) == 1
    assert qr.data_list[0][0] == "binary"
    assert isinstance(qr.data_list[0][1], str)

def test_invalid_binary_data():
    """Test invalid binary data handling."""
    qr = QRCodeX()
    with pytest.raises(QRCodeXError):
        qr.add_data("not bytes", data_type="binary")

def test_url_detection():
    """Test automatic URL detection."""
    qr = QRCodeX()
    qr.add_data("https://example.com")
    assert len(qr.data_list) == 1
    assert qr.data_list[0][0] == "url"

def test_image_data(tmp_path):
    """Test image data handling."""
    # Create a test image
    img_path = tmp_path / "test.png"
    img = Image.new('RGB', (10, 10), color='red')
    img.save(img_path)
    
    qr = QRCodeX()
    qr.add_data(img_path, data_type="image")
    assert len(qr.data_list) == 1
    assert qr.data_list[0][0] == "image"
    assert qr.data_list[0][1].startswith("data:image/png;base64,")

def test_invalid_image_path():
    """Test invalid image path handling."""
    qr = QRCodeX()
    with pytest.raises(QRCodeXError):
        qr.add_data("nonexistent.png", data_type="image")

def test_invalid_output_format():
    """Test invalid output format handling."""
    qr = QRCodeX()
    qr.add_data("test")
    with pytest.raises(QRCodeXError):
        qr.generate("test.jpg", format="jpg")

def test_invalid_colors():
    """Test invalid color handling."""
    qr = QRCodeX()
    qr.add_data("test")
    with pytest.raises(QRCodeXError):
        qr.generate("test.png", fill_color="invalid")
    with pytest.raises(QRCodeXError):
        qr.generate("test.png", back_color="invalid")

def test_multiple_data():
    """Test multiple data handling."""
    qr = QRCodeX()
    qr.add_data("text1", data_type="text")
    qr.add_data("text2", data_type="text")
    assert len(qr.data_list) == 2

def test_clear():
    """Test clear functionality."""
    qr = QRCodeX()
    qr.add_data("test")
    qr.clear()
    assert len(qr.data_list) == 0

def test_svg_generation(tmp_path):
    """Test SVG generation."""
    output = tmp_path / "test.svg"
    qr = QRCodeX()
    qr.add_data("test")
    qr.generate(output, format="svg")
    assert output.exists()
    with open(output) as f:
        content = f.read()
        assert content.startswith('<?xml')
        assert 'svg' in content

def test_large_data():
    """Test handling of large data."""
    qr = QRCodeX(error_correction='L')  # Use lowest error correction for maximum capacity
    data = "x" * 1000  # Large but should still fit
    qr.add_data(data)
    assert len(qr.data_list) == 1

def test_very_large_data():
    """Test handling of very large data."""
    qr = QRCodeX()
    data = "x" * 1000000  # Too large to fit
    with pytest.raises(QRCodeXError):
        qr.add_data(data)
        qr.generate("test.png") 