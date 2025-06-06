# python-heic-png

A Python utility to convert HEIC (High Efficiency Image Container) files to PNG format. This tool is particularly useful for users who need to convert images from Apple devices (which commonly use HEIC format) to the more widely supported PNG format.

## Features

- Convert HEIC files to PNG format
- Maintain image quality during conversion
- Simple command-line interface
- Batch processing support

## Requirements

- Python 3.6 or higher
- Pillow (PIL Fork)
- pillow-heif

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/python-heic-png.git
cd python-heic-png
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from heic_to_png import convert_heic_to_png

# Convert a single file
convert_heic_to_png('input.heic', 'output.png')

# Convert multiple files
convert_heic_to_png('input.heic', 'output.png', batch=True)
```

### Command Line Usage

```bash
python heic_to_png.py input.heic output.png
```

## How It Works

This tool uses the `pillow-heif` library to read HEIC files and the `Pillow` library to save them as PNG files. The conversion process maintains the original image quality while providing compatibility with systems that don't support HEIC format.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the Pillow and pillow-heif developers for their excellent libraries
- Inspired by the need to easily convert HEIC images from iOS devices
