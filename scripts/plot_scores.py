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
        description="Plot subjective LoRA-weight scores across multiple seeds."
    )
    parser.add_argument("--input", required=True, help="Path to the CSV score file.")
    parser.add_argument(
        "--output-dir", required=True, help="Directory where chart images will be saved."
    )
    return parser.parse_args()


def validate_scores(data: pd.DataFrame) -> None:
    required_columns = {"seed", "lora_weight", "notes", *SCORE_COLUMNS}
    missing_columns = required_columns - set(data.columns)
    if missing_columns:
        raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing_columns))}")

    for column in SCORE_COLUMNS:
        if data[column].isna().any():
            raise ValueError(f"Column '{column}' contains empty scores.")
        if not data[column].between(1, 5).all():
            raise ValueError(f"Column '{column}' must only contain scores from 1 to 5.")


def make_by_seed_chart(data: pd.DataFrame, output_path: Path) -> None:
    """Plot each seed with a small horizontal display offset for visibility."""
    # Offsets only separate coincident points visually; CSV weights remain unchanged.
    seed_styles = [
        {"offset": -0.018, "color": "#1f77b4", "marker": "o", "linestyle": "-"},
        {"offset": 0.000, "color": "#ff7f0e", "marker": "s", "linestyle": "--"},
        {"offset": 0.018, "color": "#2ca02c", "marker": "^", "linestyle": ":"},
    ]
    seeds = sorted(data["seed"].unique())

    if len(seeds) > len(seed_styles):
        raise ValueError(
            f"This chart supports at most {len(seed_styles)} seeds, "
            f"but the CSV contains {len(seeds)}."
        )

    figure, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=True)
    for axis, column in zip(axes.flatten(), SCORE_COLUMNS):
        for seed, style in zip(seeds, seed_styles):
            group = data[data["seed"] == seed].sort_values("lora_weight")
            x_values = group["lora_weight"] + style["offset"]

            axis.plot(
                x_values,
                group[column],
                color=style["color"],
                marker=style["marker"],
                linestyle=style["linestyle"],
                linewidth=2,
                markersize=7,
                markeredgecolor="black",
                markeredgewidth=0.6,
                label=f"seed {seed}",
            )

        axis.set_title(DISPLAY_NAMES[column])
        axis.set_xlabel("LoRA weight")
        axis.set_ylabel("Score (1-5)")
        axis.set_xticks(sorted(data["lora_weight"].unique()))
        axis.set_yticks([1, 2, 3, 4, 5])
        axis.set_ylim(0.8, 5.2)
        axis.grid(True, alpha=0.3)

    axes.flatten()[0].legend(title="Seed", loc="best")
    figure.suptitle(
        "LoRA Weight Sweep: Scores by Seed\n"
        "(points are slightly horizontally offset only for visibility)",
        fontsize=15,
    )
    figure.tight_layout()
    figure.savefig(output_path, dpi=180)
    plt.close(figure)


def make_mean_chart(data: pd.DataFrame, output_path: Path) -> None:
    summary = data.groupby("lora_weight")[SCORE_COLUMNS].agg(["mean", "std"]).sort_index()
    figure, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=True)
    for axis, column in zip(axes.flatten(), SCORE_COLUMNS):
        means = summary[(column, "mean")]
        stds = summary[(column, "std")].fillna(0)
        axis.errorbar(means.index, means, yerr=stds, marker="o", linewidth=2, capsize=5)
        axis.set_title(DISPLAY_NAMES[column])
        axis.set_xlabel("LoRA weight")
        axis.set_ylabel("Mean score (1-5)")
        axis.set_xticks(means.index)
        axis.set_yticks([1, 2, 3, 4, 5])
        axis.set_ylim(0.8, 5.2)
        axis.grid(True, alpha=0.3)
    figure.suptitle("LoRA Weight Sweep: Mean Scores Across Seeds (error bars = standard deviation)", fontsize=14)
    figure.tight_layout()
    figure.savefig(output_path, dpi=180)
    plt.close(figure)


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    if not input_path.is_file():
        raise FileNotFoundError(f"CSV file does not exist: {input_path}")

    data = pd.read_csv(input_path)
    validate_scores(data)
    output_dir.mkdir(parents=True, exist_ok=True)
    make_by_seed_chart(data, output_dir / "score-curves-by-seed.png")
    make_mean_chart(data, output_dir / "score-curves-mean.png")
    print(f"Saved charts for {len(data)} rows and {data['seed'].nunique()} seeds to: {output_dir}")


if __name__ == "__main__":
    main()
