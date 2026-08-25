import pandas as pd
from pathlib import Path

DATA_DIR = Path(r"D:\Dataset\Capstone_Dataset")


def merge_split(split):
    positive_file = DATA_DIR / f"{split}_positive_subset.csv"
    negative_file = DATA_DIR / f"{split}_negative_pairs.csv"
    output_file = DATA_DIR / f"{split}_pairs.csv"

    positive = pd.read_csv(positive_file)
    negative = pd.read_csv(negative_file)

    # Explicit binary label for the clone verification task
    positive["pair_label"] = 1
    negative["pair_label"] = 0

    # Make sure both dataframes have the same columns
    all_columns = list(dict.fromkeys(
        list(positive.columns) + list(negative.columns)
    ))

    for column in all_columns:
        if column not in positive.columns:
            positive[column] = None

        if column not in negative.columns:
            negative[column] = None

    positive = positive[all_columns]
    negative = negative[all_columns]

    # Merge and shuffle reproducibly
    merged = pd.concat(
        [positive, negative],
        ignore_index=True
    )

    merged = merged.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    merged.to_csv(output_file, index=False)

    print(f"{split}:")
    print(f"  Total pairs: {len(merged):,}")
    print(f"  Clone:      {(merged['pair_label'] == 1).sum():,}")
    print(f"  Non-clone:  {(merged['pair_label'] == 0).sum():,}")
    print(f"  Saved to:   {output_file}")
    print()


if __name__ == "__main__":
    for split in ["train", "val", "test"]:
        merge_split(split)

    print("Dataset merging completed.")
