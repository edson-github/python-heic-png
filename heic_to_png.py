#!/usr/bin/env python3

import sys
import argparse
from pathlib import Path
from typing import Union, List
from PIL import Image
import pillow_heif
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing


def convert_heic_to_png(
    input_path: Union[str, Path],
    output_path: Union[str, Path] = None,
    batch: bool = False
) -> Union[str, List[str]]:
    """
    Convert HEIC image(s) to PNG format.

    Args:
        input_path: Path to input HEIC file or directory
        output_path: Path to output PNG file or directory (optional)
        batch: If True, process all HEIC files in input directory

    Returns:
        Path(s) to converted PNG file(s)
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input path does not exist: {input_path}")

    if batch:
        if not input_path.is_dir():
            raise ValueError("Input path must be a directory when batch=True")

        output_path = (
            Path(output_path) if output_path
            else input_path / "converted"
        )
        output_path.mkdir(parents=True, exist_ok=True)

        heic_files = list(input_path.glob("*.heic"))
        if not heic_files:
            return []

        # Use ThreadPoolExecutor for parallel processing
        max_workers = min(multiprocessing.cpu_count(), len(heic_files))
        converted_files = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(
                    _convert_single_file,
                    heic_file,
                    output_path / f"{heic_file.stem}.png"
                ): heic_file for heic_file in heic_files
            }

            for future in as_completed(future_to_file):
                try:
                    output_file = future.result()
                    converted_files.append(str(output_file))
                except Exception as e:
                    print(
                        f"Error processing {future_to_file[future]}: {str(e)}",
                        file=sys.stderr
                    )

        return converted_files

    else:
        if not input_path.is_file():
            raise ValueError("Input path must be a file when batch=False")

        output_path = (
            Path(output_path) if output_path
            else input_path.with_suffix('.png')
        )
        if output_path.is_dir():
            output_path = output_path / f"{input_path.stem}.png"

        _convert_single_file(input_path, output_path)
        return str(output_path)


def _convert_single_file(input_file: Path, output_file: Path) -> Path:
    """
    Convert a single HEIC file to PNG.
    Args:
        input_file: Path to input HEIC file
        output_file: Path to output PNG file
    Returns:
        Path to the converted file
    """
    try:
        pillow_heif.register_heif_opener()

        with Image.open(input_file) as img:
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            img.save(output_file, 'PNG', optimize=True, quality=95)
            return output_file

    except Exception as e:
        raise Exception(f"Error converting {input_file}: {str(e)}")


def main():
    parser = argparse.ArgumentParser(
        description='Convert HEIC images to PNG format'
    )
    parser.add_argument('input', help='Input HEIC file or directory')
    parser.add_argument(
        'output',
        nargs='?',
        help='Output PNG file or directory (optional)'
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Process all HEIC files in input directory'
    )

    args = parser.parse_args()
    try:
        result = convert_heic_to_png(args.input, args.output, args.batch)
        if isinstance(result, list):
            print(f"Successfully converted {len(result)} files:")
            for file in result:
                print(f"  - {file}")
        else:
            print(f"Successfully converted to: {result}")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
