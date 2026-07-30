import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def find_images(input_dir: Path, output_path: Path) -> list[Path]:
    """Find supported input images, excluding the output file itself."""
    output_path = output_path.resolve()
    images = [
        path
        for path in input_dir.iterdir()
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_EXTENSIONS
        and path.resolve() != output_path
    ]
    return sorted(images, key=lambda path: path.name)


def make_grid(
    image_paths: list[Path], output_path: Path, columns: int, cell_width: int
) -> None:
    """Create a labeled image grid and save it to output_path."""
    if not image_paths:
        raise ValueError("No supported images found in the input directory.")

    opened_images = [
        (image_path, Image.open(image_path).convert("RGB"))
        for image_path in image_paths
    ]
    first_image = opened_images[0][1]
    cell_height = round(cell_width * first_image.height / first_image.width)
    padding = 20
    label_height = 30
    rows = math.ceil(len(opened_images) / columns)

    grid_width = columns * cell_width + (columns + 1) * padding
    grid_height = rows * (cell_height + label_height) + (rows + 1) * padding
    grid = Image.new("RGB", (grid_width, grid_height), color="white")
    draw = ImageDraw.Draw(grid)
    font = ImageFont.load_default()

    for index, (image_path, image) in enumerate(opened_images):
        row = index // columns
        column = index % columns
        x = padding + column * (cell_width + padding)
        y = padding + row * (cell_height + label_height + padding)
        resized = image.resize((cell_width, cell_height), Image.Resampling.LANCZOS)
        grid.paste(resized, (x, y))
        draw.text((x, y + cell_height + 8), image_path.stem, fill="black", font=font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    grid.save(output_path, quality=95)
    print(f"Saved grid with {len(image_paths)} images to: {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a labeled image comparison grid.")
    parser.add_argument("--input", required=True, help="Folder containing input images.")
    parser.add_argument("--output", required=True, help="Path for the output grid image.")
    parser.add_argument("--columns", type=int, default=3, help="Number of grid columns.")
    parser.add_argument(
        "--cell-width", type=int, default=420,
        help="Width of each image cell in pixels. Default: 420.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input)
    output_path = Path(args.output)
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input directory does not exist: {input_dir}")
    make_grid(
        image_paths=find_images(input_dir, output_path),
        output_path=output_path,
        columns=args.columns,
        cell_width=args.cell_width,
    )


if __name__ == "__main__":
    main()
