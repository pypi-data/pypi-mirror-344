"""QR Code generator implementation."""

from typing import Union, Optional, List, Tuple
from pathlib import Path
from PIL import Image
import base64
import re
from io import BytesIO

from .exceptions import (
    QRCodeXError, QRCodeXValueError, QRCodeXTypeError,
    QRCodeXDataError, QRCodeXCapacityError, QRCodeXImageError
)
from .utils import (
    validate_color, validate_size, validate_path,
    image_to_data_uri, detect_data_type
)
from .capacity import ErrorCorrectionLevel, get_minimum_version
from .qr_algorithm import QRCode, QRMode

# Maximum data capacity for QR code version 40 with low error correction
MAX_DATA_CAPACITY = 2953

class QRCodeX:
    """Advanced QR Code generator with multiple data type support."""
    
    ERROR_CORRECTION_MAP = {
        'L': ErrorCorrectionLevel.L,
        'M': ErrorCorrectionLevel.M,
        'Q': ErrorCorrectionLevel.Q,
        'H': ErrorCorrectionLevel.H
    }
    
    def __init__(
        self,
        error_correction: str = 'M',
        box_size: int = 10,
        border: int = 4,
        version: Optional[int] = None
    ):
        """Initialize QRCodeX generator.
        
        Args:
            error_correction: Error correction level ('L', 'M', 'Q', 'H')
            box_size: Size of each QR code module in pixels
            border: Border size in modules
            version: QR code version (1-40), or None for auto
            
        Raises:
            QRCodeXError: If any parameters are invalid
        """
        # Validate error correction level
        if error_correction not in ['L', 'M', 'Q', 'H']:
            raise QRCodeXError(
                f"Invalid error correction level: {error_correction}. "
                "Must be one of: L, M, Q, H"
            )
        
        # Validate box size
        if not isinstance(box_size, (int, float)) or box_size < 1:
            raise QRCodeXError(
                f"Invalid box size: {box_size}. Must be a positive number"
            )
            
        # Validate border
        if not isinstance(border, (int, float)) or border < 0:
            raise QRCodeXError(
                f"Invalid border size: {border}. Must be a non-negative number"
            )
            
        # Validate version if provided
        if version is not None:
            if not isinstance(version, int) or version < 1 or version > 40:
                raise QRCodeXError(
                    f"Invalid version: {version}. Must be between 1 and 40"
                )
                
        self.error_correction = error_correction
        self.box_size = int(box_size)
        self.border = int(border)
        self.version = version
        self._qr = None
        self.data_list: List[Tuple[str, str]] = []
    
    def add_data(self, data: Union[str, bytes, Path], data_type: str = None) -> None:
        """Add data to the QR code.
        
        Args:
            data: The data to encode (string, bytes, or Path to image)
            data_type: Type of data ('text', 'url', 'image', 'binary', or None for auto)
            
        Raises:
            QRCodeXError: If data or data_type is invalid
            QRCodeXCapacityError: If data is too large for QR code
        """
        if data is None:
            raise QRCodeXError("Data cannot be None")
            
        # Auto-detect data type if not specified
        if data_type is None:
            if isinstance(data, bytes):
                data_type = 'binary'
            elif isinstance(data, Path):
                data_type = 'image'
            elif isinstance(data, str):
                if re.match(r'^https?://', data):
                    data_type = 'url'
                else:
                    data_type = 'text'
            else:
                raise QRCodeXError(f"Cannot auto-detect type for data: {type(data)}")
                
        # Validate data type
        valid_types = ['text', 'url', 'image', 'binary']
        if data_type not in valid_types:
            raise QRCodeXError(
                f"Invalid data type: {data_type}. Must be one of: {', '.join(valid_types)}"
            )
            
        # Process data based on type
        processed_data = self._process_data(data, data_type)
        
        # Check data capacity
        total_data_length = sum(len(d[1]) for d in self.data_list) + len(processed_data)
        if total_data_length > MAX_DATA_CAPACITY:
            raise QRCodeXError(
                f"Data too large for QR code. Maximum capacity is {MAX_DATA_CAPACITY} bytes"
            )
            
        self.data_list.append((data_type, processed_data))
        self._qr = None
    
    def _process_data(self, data: Union[str, bytes, Path], data_type: str) -> str:
        """Process data based on its type.
        
        Args:
            data: Raw data to process
            data_type: Type of data
            
        Returns:
            Processed data as string
            
        Raises:
            QRCodeXError: If data processing fails
        """
        try:
            if data_type == 'binary':
                if not isinstance(data, bytes):
                    raise QRCodeXError("Binary data must be bytes")
                return base64.b64encode(data).decode('ascii')
                
            elif data_type == 'image':
                if isinstance(data, str) and data.startswith('data:image/'):
                    return data
                try:
                    if isinstance(data, Path):
                        img = Image.open(data)
                    else:
                        raise QRCodeXError("Image data must be Path or data URI")
                    # Convert image to data URI
                    img_bytes = BytesIO()
                    img.save(img_bytes, format='PNG')
                    b64_data = base64.b64encode(img_bytes.getvalue()).decode('ascii')
                    return f"data:image/png;base64,{b64_data}"
                except Exception as e:
                    raise QRCodeXError(f"Failed to process image: {str(e)}")
                    
            elif data_type in ['text', 'url']:
                if not isinstance(data, str):
                    raise QRCodeXError(f"{data_type} data must be string")
                return data
                
            else:
                raise QRCodeXError(f"Unknown data type: {data_type}")
                
        except Exception as e:
            raise QRCodeXError(f"Failed to process {data_type} data: {str(e)}")
    
    def generate(
        self,
        output_path: Union[str, Path],
        fill_color: str = "black",
        back_color: str = "white",
        format: str = "png"
    ) -> None:
        """Generate QR code and save to file.
        
        Args:
            output_path: Path to save the QR code
            fill_color: Color of QR code modules
            back_color: Background color
            format: Output format ('png' or 'svg')
            
        Raises:
            QRCodeXError: If generation fails
        """
        # Validate colors
        validate_color(fill_color)
        validate_color(back_color)
        
        # Validate format
        if format.lower() not in ['png', 'svg']:
            raise QRCodeXError(f"Unsupported format: {format}")
            
        # Validate we have data
        if not self.data_list:
            raise QRCodeXError("No data added to QR code")
            
        try:
            # Generate QR code
            qr = self._generate_qr()
            
            # Save to file
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if format.lower() == 'svg':
                self._save_svg(qr, output_path, fill_color)
            else:
                self._save_png(qr, output_path, fill_color, back_color)
                
        except Exception as e:
            raise QRCodeXError(f"Failed to generate QR code: {str(e)}")
    
    def _generate_qr(self):
        if self._qr is None:
            self._qr = QRCode(
                version=self.version,
                error_correction=self.error_correction
            )
            
            # Add all data
            for _, data in self.data_list:
                self._qr.add_data(data)
            
            self._qr.make(fit=True)
        
        return self._qr
    
    def _save_svg(self, qr, output_path, fill_color):
        result = qr.make_image(
            fill_color=fill_color,
            back_color="white",
            format="SVG"
        )
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
    
    def _save_png(self, qr, output_path, fill_color, back_color):
        result = qr.make_image(
            fill_color=fill_color,
            back_color=back_color,
            format="PNG"
        )
        result.save(output_path)
    
    def clear(self) -> None:
        """Clear all data from the QR code."""
        self.data_list.clear()
        self._qr = None
        self.version = None 