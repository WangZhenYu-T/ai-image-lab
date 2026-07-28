import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def find_images(input_dir: Path) -> list[Path]:
    """Find supported image files in the input directory, sorted by filename."""
    images = [
        path
        for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return sorted(images, key=lambda path: path.name)


def make_grid(
    image_paths: list[Path],
    output_path: Path,
    columns: int,
    cell_width: int,
    padding: int,
    label_height: int,
) -> None:
    """Create a labeled image grid and save it to output_path."""
    if not image_paths:
        raise ValueError("No supported images found in the input directory.")

    opened_images = []
    for image_path in image_paths:
        image = Image.open(image_path).convert("RGB")
        opened_images.append((image_path, image))

    # Use the first image's aspect ratio to determine a uniform cell height.
    first_image = opened_images[0][1]
    cell_height = round(cell_width * first_image.height / first_image.width)

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

        label = image_path.stem
        label_x = x
        label_y = y + cell_height + 8
        draw.text((label_x, label_y), label, fill="black", font=font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    grid.save(output_path, quality=95)
    print(f"Saved grid with {len(image_paths)} images to: {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a labeled image comparison grid."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Folder containing PNG, JPG, JPEG, or WebP images.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path for the output grid image, for example assets/grid.jpg.",
    )
    parser.add_argument(
        "--columns",
        type=int,
        default=3,
        help="Number of columns in the grid. Default: 3.",
    )
    parser.add_argument(
        "--cell-width",
        type=int,
        default=420,
        help="Width of each image cell in pixels. Default: 360.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_dir = Path(args.input)
    output_path = Path(args.output)

    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input directory does not exist: {input_dir}")

    make_grid(
        image_paths=find_images(input_dir),
        output_path=output_path,
        columns=args.columns,
        cell_width=args.cell_width,
        padding=20,
        label_height=30,
    )


if __name__ == "__main__":
    main()