import pandas as pd
from pathlib import Path

DATA_DIR = Path(r"D:\Dataset\Capstone_Dataset")

TARGETS = {
    "train": 3000,
    "val": 750,
    "test": 1000,
}


def select_diverse_subset(df: pd.DataFrame, target_size: int, seed: int = 42):
    """
    Select a reproducible subset while trying to preserve
    diversity across program IDs.
    """
    if target_size >= len(df):
        return df.sample(frac=1, random_state=seed).reset_index(drop=True)

    # Shuffle first
    shuffled = df.sample(frac=1, random_state=seed).reset_index(drop=True)

    # First, take at most one pair from each program
    first_pass = (
        shuffled
        .drop_duplicates(subset=["program_id"], keep="first")
        .copy()
    )

    selected = first_pass.iloc[:target_size].copy()

    # If we still need more rows, fill from remaining pairs
    if len(selected) < target_size:
        selected_ids = set(selected["pair_id"])

        remaining = shuffled[
            ~shuffled["pair_id"].isin(selected_ids)
        ]

        extra_needed = target_size - len(selected)

        extra = remaining.sample(
            n=min(extra_needed, len(remaining)),
            random_state=seed
        )

        selected = pd.concat([selected, extra], ignore_index=True)

    return selected.sample(frac=1, random_state=seed).reset_index(drop=True)


for split, target in TARGETS.items():
    input_file = DATA_DIR / f"{split}_positive_pairs.csv"
    output_file = DATA_DIR / f"{split}_positive_subset.csv"

    df = pd.read_csv(input_file)

    subset = select_diverse_subset(
        df,
        target_size=target,
        seed=42
    )

    subset.to_csv(output_file, index=False)

    print(f"{split}:")
    print(f"  Original pairs : {len(df):,}")
    print(f"  Selected pairs : {len(subset):,}")
    print(f"  Unique programs: {subset['program_id'].nunique():,}")
    print(f"  Saved to       : {output_file}")
    print()

