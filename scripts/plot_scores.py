import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


SCORE_COLUMNS = [
    "style_strength",
    "aesthetic_quality",
    "coordination",
    "artifact_level",
]

DISPLAY_NAMES = {
    "style_strength": "Style strength",
    "aesthetic_quality": "Aesthetic quality",
    "coordination": "Coordination",
    "artifact_level": "Artifact level (higher is worse)",
}

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot subjective scores against LoRA weight."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the CSV score file.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path for the output chart image.",
    )
    return parser.parse_args()


def validate_scores(data: pd.DataFrame) -> None:
    required_columns = {"seed", "lora_weight", "notes", *SCORE_COLUMNS}
    missing_columns = required_columns - set(data.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"CSV is missing required columns: {missing}")

    for column in SCORE_COLUMNS:
        if data[column].isna().any():
            raise ValueError(f"Column '{column}' contains empty scores.")

        invalid_scores = data[~data[column].between(1, 5)]
        if not invalid_scores.empty:
            raise ValueError(
                f"Column '{column}' must only contain scores from 1 to 5."
            )


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.is_file():
        raise FileNotFoundError(f"CSV file does not exist: {input_path}")

    data = pd.read_csv(input_path)
    validate_scores(data)

    data = data.sort_values("lora_weight")

    plt.figure(figsize=(9, 5))

    for column in SCORE_COLUMNS:
        plt.plot(
            data["lora_weight"],
            data[column],
            marker="o",
            linewidth=2,
            label=DISPLAY_NAMES[column],
        )

    plt.title("LoRA Weight Sweep: Subjective Scores")
    plt.xlabel("LoRA weight")
    plt.ylabel("Score (1-5)")
    plt.xticks(data["lora_weight"])
    plt.yticks([1, 2, 3, 4, 5])
    plt.ylim(0.8, 5.2)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=180)
    plt.close()

    print(f"Saved score chart for {len(data)} rows to: {output_path}")


if __name__ == "__main__":
    main()