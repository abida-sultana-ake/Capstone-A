import csv
from pathlib import Path


# XLCoST Java-Python dataset location
XL_DIR = Path(
    r"D:\Dataset\XLCoST_data\generation\pair_data_tok_1\Java-Python"
)
# Where we will save our Capstone dataset
OUTPUT_DIR = Path(r"D:\Dataset\Capstone_Dataset")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def read_lines(path: Path):
    """Read a text file and return one entry per line."""
    with path.open("r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def make_positive_pairs(split: str):
    """
    Create aligned Java-Python positive pairs from XLCoST.

    XLCoST's map files and tokenized source files are line-aligned:
        Java-map line i <-> Java code line i
        Python-map line i <-> Python code line i
    """

    java_map_path = XL_DIR / f"{split}-Java-map.jsonl"
    python_map_path = XL_DIR / f"{split}-Python-map.jsonl"

    java_code_path = XL_DIR / f"{split}-Java-Python-tok.java"
    python_code_path = XL_DIR / f"{split}-Java-Python-tok.py"

    # Make sure all required files exist
    required_files = [
        java_map_path,
        python_map_path,
        java_code_path,
        python_code_path,
    ]

    for path in required_files:
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

    # Read files
    java_map = read_lines(java_map_path)
    python_map = read_lines(python_map_path)

    java_code = read_lines(java_code_path)
    python_code = read_lines(python_code_path)

    # Safety check: all files must have same number of lines
    lengths = {
        "java_map": len(java_map),
        "python_map": len(python_map),
        "java_code": len(java_code),
        "python_code": len(python_code),
    }

    if len(set(lengths.values())) != 1:
        raise ValueError(
            f"{split}: line counts do not match: {lengths}"
        )

    rows = []

    for i, (java_id, python_id, java_src, python_src) in enumerate(
        zip(java_map, python_map, java_code, python_code),
        start=1,
    ):
        # Example:
        # 10005-Java-1
        # 10005-Python-1
        #
        # The first part is the underlying problem/program ID.
        java_parts = java_id.split("-")
        python_parts = python_id.split("-")

        if len(java_parts) < 3 or len(python_parts) < 3:
            raise ValueError(
                f"Unexpected ID format:\n"
                f"Java: {java_id}\n"
                f"Python: {python_id}"
            )

        # Make sure both snippets belong to the same underlying problem
        if java_parts[0] != python_parts[0]:
            raise ValueError(
                f"Alignment mismatch at line {i}: "
                f"{java_id} vs {python_id}"
            )

        program_id = java_parts[0]

        rows.append(
            {
                "pair_id": f"{split.upper()}_POS_{i:06d}",
                "program_id": program_id,
                "java_id": java_id,
                "python_id": python_id,
                "language_a": "Java",
                "language_b": "Python",
                "code_a": java_src,
                "code_b": python_src,
                "label": 1,
                "pair_type": "positive",
                "split": split,
                "source": "XLCoST",
            }
        )

    output_file = OUTPUT_DIR / f"{split}_positive_pairs.csv"

    fieldnames = list(rows[0].keys())

    with output_file.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"{split}: created {len(rows):,} positive pairs")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    print("Creating Java-Python positive pairs from XLCoST...\n")

    for split in ["train", "val", "test"]:
        make_positive_pairs(split)

    print("\nDone.")