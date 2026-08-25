# Capstone-A Dataset Construction

## 1. Overview

This folder contains the dataset construction output for the Capstone-A project on:

**Explainable Cross-Language Code Clone Detection and Maintenance Decision Support**

The dataset focuses on **Java–Python cross-language code pairs** and is constructed using the **XLCoST (Cross-lingual Code Intelligence) benchmark dataset**.

The dataset is intended for the **Clone / Non-Clone verification stage** of the project.

> **Important:** The labels in this dataset do not represent developer intent, Good/Bad clones, or maintenance risk.

---

## 2. Source Dataset

### XLCoST

**Dataset:** XLCoST: A Benchmark Dataset for Cross-lingual Code Intelligence

**Used languages:**

- Java
- Python

XLCoST provides aligned cross-language code data at snippet and program levels.

Official repository:

https://github.com/reddy-lab-code-research/XLCoST

Paper:

Zhu, M., Jain, A., Suresh, K., Ravindran, R., Tipirneni, S., & Reddy, C. K. (2022).  
**XLCoST: A Benchmark Dataset for Cross-lingual Code Intelligence.**

---

## 3. Dataset Construction

The dataset was constructed in four main steps:

```text
XLCoST
   ↓
Java–Python aligned pairs
   ↓
Positive pair extraction
   ↓
Positive subset selection
   ↓
Different-program negative pair construction
   ↓
Positive + Negative merge
   ↓
Final Train / Validation / Test Dataset
````

---

## 4. Positive Pair Construction

The Java–Python aligned data was obtained from the XLCoST Java–Python dataset.

Relevant source:

```text
generation/
└── pair_data_tok_1/
    └── Java-Python/
```

The following files were used for the three official dataset splits:

```text
train-Java-map.jsonl
train-Python-map.jsonl
train-Java-Python-tok.java
train-Java-Python-tok.py

val-Java-map.jsonl
val-Python-map.jsonl
val-Java-Python-tok.java
val-Java-Python-tok.py

test-Java-map.jsonl
test-Python-map.jsonl
test-Java-Python-tok.java
test-Java-Python-tok.py
```

The Java and Python map files are line-aligned with their corresponding tokenized code files.

For example:

```text
10005-Java-1
10005-Python-1
```

represents an aligned Java–Python pair.

These aligned pairs were assigned:

```text
label = 1
pair_type = positive
```

### Original Extracted Positive Data

| Split      | Positive Pairs |
| ---------- | -------------: |
| Train      |         77,759 |
| Validation |          3,938 |
| Test       |          7,259 |
| **Total**  |     **88,956** |

---

## 5. Positive Subset Selection

The complete 88,956 positive pairs were larger than necessary for the initial Capstone experiment.

Therefore, a smaller reproducible subset was selected from each official XLCoST split using a fixed random seed (`42`).

| Split      | Selected Positive Pairs |
| ---------- | ----------------------: |
| Train      |                   3,000 |
| Validation |                     750 |
| Test       |                   1,000 |

Intermediate files created during this step:

```text
train_positive_subset.csv
val_positive_subset.csv
test_positive_subset.csv
```

---

## 6. Negative Pair Construction

Negative examples were constructed by pairing Java and Python snippets associated with different benchmark program IDs.

For example:

```text
Java Program A
        +
Python Program B
```

where:

```text
Program A != Program B
```

was treated as a negative pair.

Negative pairs were generated separately within the official training, validation, and test splits.

A sanity check confirmed that no negative pair used the same program ID on both sides.

```text
Same-program negative pairs = 0
```

These pairs were assigned:

```text
label = 0
pair_type = negative
```

Intermediate files:

```text
train_negative_pairs.csv
val_negative_pairs.csv
test_negative_pairs.csv
```

---

## 7. Final Dataset

The positive and negative pairs were merged separately for the training, validation, and test sets.

| Split      | Positive / Clone | Negative / Non-Clone |     Total |
| ---------- | ---------------: | -------------------: | --------: |
| Train      |            3,000 |                3,000 |     6,000 |
| Validation |              750 |                  750 |     1,500 |
| Test       |            1,000 |                1,000 |     2,000 |
| **Total**  |        **4,750** |            **4,750** | **9,500** |

### Class Distribution

```text
Positive / Clone     = 4,750
Negative / Non-Clone = 4,750
Class Balance        = 50% / 50%
```

The final dataset files are:

```text
train_pairs.csv
val_pairs.csv
test_pairs.csv
```

---

## 8. Dataset Columns

The final pair files contain fields such as:

```text
pair_id
program_id
java_id
python_id
language_a
language_b
code_a
code_b
label
pair_type
split
source
pair_label
program_id_a
program_id_b
```

### Important Fields

| Field        | Description                                      |
| ------------ | ------------------------------------------------ |
| `pair_id`    | Unique identifier for the pair                   |
| `program_id` | Underlying program ID for aligned positive pairs |
| `java_id`    | Java snippet identifier                          |
| `python_id`  | Python snippet identifier                        |
| `code_a`     | Java tokenized code                              |
| `code_b`     | Python tokenized code                            |
| `pair_label` | Final binary label                               |
| `pair_type`  | Positive or negative                             |
| `split`      | Train, validation, or test                       |
| `source`     | Dataset source                                   |

For negative pairs, `program_id` may be empty because the two snippets originate from different programs. Their individual program IDs are stored in:

```text
program_id_a
program_id_b
```

---

## 9. Label Definition

The final dataset uses:

```text
1 = Positive / aligned cross-language pair
0 = Negative / different-program pair
```

These labels are intended for the **cross-language clone verification stage**.

They do not represent:

```text
Good Clone
Bad Clone
Intentional Clone
Unintentional Clone
High Maintenance Risk
Low Maintenance Risk
```

No large-scale manual developer-intent annotation was performed.

---

## 10. Reproducibility

The following scripts are included in the dataset handover folder:

```text
make_positive_pairs.py
make_positive_subset.py
make_negative_pairs.py
merge_datasets.py
```

### Script Responsibilities

**`make_positive_pairs.py`**

Extracts aligned Java–Python positive pairs from XLCoST.

**`make_positive_subset.py`**

Selects the smaller reproducible positive subset used for the Capstone experiment.

**`make_negative_pairs.py`**

Constructs Java–Python negative pairs using different benchmark program IDs.

**`merge_datasets.py`**

Combines the positive and negative examples into the final train, validation, and test datasets.

---

## 11. Dataset Construction Workflow

```text
XLCoST Java–Python Data
            ↓
Aligned Positive Pair Extraction
            ↓
Positive Subset Selection
            ↓
Different-Program Negative Pair Construction
            ↓
Positive + Negative Merge
            ↓
Balanced Dataset
            ↓
Train / Validation / Test
```

---

## 12. Dataset Limitations

The positive examples are derived from XLCoST's aligned Java–Python data.

The negative examples are constructed using the different-program criterion.

Therefore, the negative examples should be described as:

> **Constructed different-program negative pairs**

They should not be described as manually verified or professionally annotated non-clones.

A further limitation is that different programming problems can sometimes have superficially similar functionality. Future work may therefore introduce harder negative examples based on semantic similarity.

---

## 13. Final Dataset Summary

```text
Dataset Source:
XLCoST

Languages:
Java ↔ Python

Train:
6,000 pairs

Validation:
1,500 pairs

Test:
2,000 pairs

Total:
9,500 pairs

Positive:
4,750

Negative:
4,750

Class Balance:
50% / 50%
```

The final dataset is intended to support the **cross-language semantic clone verification stage** of the Capstone-A methodology.

```