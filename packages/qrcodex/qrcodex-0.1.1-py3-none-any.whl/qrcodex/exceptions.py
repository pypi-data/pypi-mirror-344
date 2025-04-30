"""Custom exceptions for QRCodeX."""

class QRCodeXError(Exception):
    """Base exception for QRCodeX."""
    pass

class QRCodeXValueError(QRCodeXError):
    """Exception raised for invalid parameter values."""
    pass

class QRCodeXTypeError(QRCodeXError):
    """Exception raised for invalid parameter types."""
    pass

class QRCodeXDataError(QRCodeXError):
    """Exception raised for invalid data."""
    pass

class QRCodeXCapacityError(QRCodeXError):
    """Exception raised when data exceeds QR code capacity."""
    pass

class QRCodeXImageError(QRCodeXError):
    """Exception raised for image-related errors."""
    pass

class QRCodeXFileError(QRCodeXError):
    """Exception raised for file-related errors."""
    pass 