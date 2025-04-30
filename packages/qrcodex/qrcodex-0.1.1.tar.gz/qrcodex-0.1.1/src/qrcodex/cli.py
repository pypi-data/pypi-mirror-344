"""Command-line interface for QRCodeX."""

import argparse
from pathlib import Path
from typing import Optional
import sys

from .generator import QRCodeX
from .exceptions import QRCodeXError

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate QR codes with multiple data types support."
    )
    
    parser.add_argument(
        "data",
        help="Data to encode (text, URL, or path to image file)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("qr.png"),
        help="Output file path (default: qr.png)"
    )
    
    parser.add_argument(
        "-t", "--type",
        choices=["text", "url", "image", "email", "phone", "wifi", "geo"],
        help="Data type (default: auto-detect)"
    )
    
    parser.add_argument(
        "-f", "--format",
        choices=["png", "svg"],
        default="png",
        help="Output format (default: png)"
    )
    
    parser.add_argument(
        "--fill-color",
        default="black",
        help="QR code color (default: black)"
    )
    
    parser.add_argument(
        "--back-color",
        default="white",
        help="Background color (default: white)"
    )
    
    parser.add_argument(
        "-e", "--error-correction",
        choices=["L", "M", "Q", "H"],
        default="H",
        help="Error correction level (default: H)"
    )
    
    parser.add_argument(
        "-s", "--box-size",
        type=int,
        default=10,
        help="Box size in pixels (default: 10)"
    )
    
    parser.add_argument(
        "-b", "--border",
        type=int,
        default=4,
        help="Border size in boxes (default: 4)"
    )
    
    parser.add_argument(
        "-v", "--version",
        type=int,
        help="QR code version (1-40, default: auto)"
    )
    
    return parser.parse_args()

def main() -> Optional[int]:
    """Main entry point for CLI."""
    args = parse_args()
    
    try:
        qr = QRCodeX(
            error_correction=args.error_correction,
            box_size=args.box_size,
            border=args.border,
            version=args.version
        )
        
        qr.add_data(args.data, data_type=args.type)
        qr.generate(
            args.output,
            fill_color=args.fill_color,
            back_color=args.back_color,
            format=args.format
        )
        
        print(f"QR code saved to: {args.output}")
        return 0
        
    except QRCodeXError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 