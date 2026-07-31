import argparse
import csv
import json
from pathlib import Path


REQUIRED_CONFIG_KEYS = {
    "experiment_id",
    "tested_lora",
    "tested_variable",
    "seeds",
    "generation",
    "fixed_loras",
    "hires_fix",
    "evaluation",
}

REQUIRED_SCORE_COLUMNS = {
    "seed",
    "lora_weight",
    "style_strength",
    "aesthetic_quality",
    "coordination",
    "artifact_level",
    "notes",
}

SCORE_COLUMNS = [
    "style_strength",
    "aesthetic_quality",
    "coordination",
    "artifact_level",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate whether an experiment config matches its score CSV."
    )
    parser.add_argument("--config", required=True, help="Path to config.json.")
    parser.add_argument("--scores", required=True, help="Path to scores.csv.")
    return parser.parse_args()


def load_config(config_path: Path) -> dict:
    try:
        with config_path.open("r", encoding="utf-8-sig") as file:
            config = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in {config_path}: line {error.lineno}, "
            f"column {error.colno}: {error.msg}"
        ) from error

    missing_keys = REQUIRED_CONFIG_KEYS - set(config)
    if missing_keys:
        raise ValueError(
            "config.json is missing required keys: "
            + ", ".join(sorted(missing_keys))
        )

    return config


def load_scores(scores_path: Path) -> list[dict]:
    with scores_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            raise ValueError("scores.csv has no header row.")

        missing_columns = REQUIRED_SCORE_COLUMNS - set(reader.fieldnames)
        if missing_columns:
            raise ValueError(
                "scores.csv is missing required columns: "
                + ", ".join(sorted(missing_columns))
            )
        rows = list(reader)

    if not rows:
        raise ValueError("scores.csv contains no data rows.")
    return rows


def validate_score_values(rows: list[dict]) -> None:
    for row_number, row in enumerate(rows, start=2):
        for column in SCORE_COLUMNS:
            try:
                score = float(row[column])
            except ValueError as error:
                raise ValueError(
                    f"Row {row_number}: '{column}' is not a number: {row[column]!r}"
                ) from error

            if not 1 <= score <= 5:
                raise ValueError(
                    f"Row {row_number}: '{column}' must be between 1 and 5, "
                    f"but got {score}."
                )


def main() -> None:
    args = parse_args()
    config_path = Path(args.config)
    scores_path = Path(args.scores)

    if not config_path.is_file():
        raise FileNotFoundError(f"Config file does not exist: {config_path}")
    if not scores_path.is_file():
        raise FileNotFoundError(f"Score file does not exist: {scores_path}")

    config = load_config(config_path)
    rows = load_scores(scores_path)
    validate_score_values(rows)

    config_seeds = {int(seed) for seed in config["seeds"]}
    csv_seeds = {int(row["seed"]) for row in rows}
    config_weights = {float(weight) for weight in config["tested_variable"]["values"]}
    csv_weights = {float(row["lora_weight"]) for row in rows}

    if config_seeds != csv_seeds:
        raise ValueError(
            "Seed mismatch:\n"
            f"  config.json: {sorted(config_seeds)}\n"
            f"  scores.csv:  {sorted(csv_seeds)}"
        )

    if config_weights != csv_weights:
        raise ValueError(
            "Weight mismatch:\n"
            f"  config.json: {sorted(config_weights)}\n"
            f"  scores.csv:  {sorted(csv_weights)}"
        )
