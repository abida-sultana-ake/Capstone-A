# Capstone-A Handover: Java–Python Code Clone Dataset Construction

## Project Title
**Explainable Cross-Language Code Clone Detection and Maintenance Decision Support**

## Purpose of This README
This document details the dataset construction methodology, pipeline, and final data split used for the **Capstone-A** project handover. 

> **Scope Note:** This README strictly covers dataset processing, cleaning, and sampling. Downstream modeling tasks—including UniXcoder experiments, SVM/XGBoost baselines, feature extraction, embedding generation, model training, clone prioritization, and prototype development—are intentionally omitted.

---

## Dataset Source & Attribution
The cross-language pairs were derived from the **XLCoST** benchmark.

* **Benchmark Paper:**  
  Zhu, M., Jain, A., Suresh, K., Ravindran, R., Tipirneni, S., & Reddy, C. K. (2022). *XLCoST: A Benchmark Dataset for Cross-lingual Code Intelligence*.
* **Repository:** [https://github.com/reddy-lab-code-research/XLCoST](https://github.com/reddy-lab-code-research/XLCoST)
* **Target Languages:** Java and Python (program/snippet aligned).

---

## XLCoST Source Files Used
Data was extracted from the XLCoST generation directory structure:

```text
generation/
└── pair_data_tok_1/
    └── Java-Python/
        ├── train-Java-map.jsonl
        ├── train-Python-map.jsonl
        ├── train-Java-Python-tok.java
        ├── train-Java-Python-tok.py
        ├── val-Java-map.jsonl
        ├── val-Python-map.jsonl
        ├── val-Java-Python-tok.java
        ├── val-Java-Python-tok.py
        ├── test-Java-map.jsonl
        ├── test-Python-map.jsonl
        ├── test-Java-Python-tok.java
        └── test-Java-Python-tok.py

```

### Alignment Protocol

Line `N` of a `.jsonl` map file corresponds strictly to line `N` of the matching `.java` or `.py` tokenized source file. An aligned pair is formed when both snippets share matching problem IDs across languages.

* **Example Pair:** `10005-Java-1` $\leftrightarrow$ `10005-Python-1`

---

## Positive Pair Construction

Aligned Java–Python pairs from XLCoST represent semantically equivalent code across languages and are assigned the ground-truth label **`1`** (Clone).

### Full Extracted Positive Corpus

| Split | Positive Pairs |
| --- | --- |
| **Train** | 77,759 |
| **Validation** | 3,938 |
| **Test** | 7,259 |
| **Total** | **88,956** |

---

## Positive Subset Selection & Negative Generation

To create a balanced and computationally efficient dataset for downstream tasks, a representative subset of positive pairs was selected alongside synthesized non-clone (negative) pairs assigned label **`0`**.

### Negative Sampling Logic

Non-clone pairs (Label `0`) were generated via random cross-pairing of non-aligned Java and Python snippets within the same partition split. To prevent semantic overlap:

1. Java snippet $i$ and Python snippet $j$ are paired where Problem ID $(i) \neq$ Problem ID $(j)$.
2. Strict duplicate checks were applied to prevent implicit overlap across splits.

---

## Final Dataset Distribution

| Split | Positive Pairs (Label 1) | Negative Pairs (Label 0) | Total Samples |
| --- | --- | --- | --- |
| **Train** | *Subset Selected* | *Generated* | *Partition Total* |
| **Validation** | *Subset Selected* | *Generated* | *Partition Total* |
| **Test** | *Subset Selected* | *Generated* | *Partition Total* |
| **Total** | **Subset Total** | **Negative Total** | **Dataset Total** |

---

## Folder & Data Schema

### Directory Structure

```text
dataset/
├── train.jsonl
├── val.jsonl
└── test.jsonl

```

### Data Schema (`.jsonl`)

```json
{
  "pair_id": "POS_10005_1",
  "java_id": "10005-Java-1",
  "python_id": "10005-Python-1",
  "java_code": "public class Solution { ... }",
  "python_code": "class Solution: ...",
  "label": 1
}