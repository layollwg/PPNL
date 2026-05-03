# PPNL – Part 1: Single-Goal Grid Navigation Pipeline

This repository contains the **data generation, preprocessing, evaluation and sanity-check pipeline** for single-goal grid path-planning experiments (Part 1 of the PPNL project).

---

## Directory Structure

```
PPNL/
├── README.md
├── requirements.txt
├── .gitignore
├── scripts/
│   ├── generate_single_goal_data.py   # Generate IID / OOD JSONL datasets
│   ├── data_preprocess.py             # Validate & normalise to standard schema
│   ├── evaluate_executor.py           # Parse predictions + compute metrics
│   ├── sanity_check.py                # Gold-path / bad-action self-tests
│   └── utils/
│       ├── actions.py                 # Action parsing & normalisation
│       ├── grid.py                    # BFS shortest path, grid rendering
│       └── io.py                      # JSONL I/O, seed utilities
└── data/
    └── single_goal/
        ├── 6x6/
        │   ├── train.jsonl            # 1 000 IID training samples
        │   ├── valid.jsonl            #   200 IID validation samples
        │   └── test_iid.jsonl         #   200 IID test samples
        └── 6x6_dense/
            └── test_ood.jsonl         #   200 OOD (dense) test samples
```

---

## Conventions

| Concept | Value |
|---|---|
| Grid size | 6 × 6 |
| World encoding | `0` empty · `1` obstacle · `2` start · `3` goal |
| Valid actions | `up` `down` `left` `right` (lower-case) |
| Action separator | space |
| IID obstacle density | 10 – 25 % of all cells |
| OOD obstacle density | 35 – 50 % of all cells |
| Coordinate system | `(row, col)`, 0-indexed, origin top-left |
| Movement | `up` → row−1 · `down` → row+1 · `left` → col−1 · `right` → col+1 |

---

## JSONL Schema

Each line in every data file is a JSON object with the following fields:

```json
{
  "id":          "train_000001",
  "grid_size":   [6, 6],
  "world":       [[0,0,0,0,1,2], "..."],
  "start":       [0, 5],
  "goal":        [3, 2],
  "input_coord": "Grid 6x6. Start: (row=0, col=5). Goal: (row=3, col=2). Obstacles: [(0,4), ...].",
  "input_grid":  ". . . . # S\n. . . # . .\n...",
  "target":      "down down left left down left",
  "meta": {
    "obstacle_count":   7,
    "obstacle_density": 0.1944,
    "path_length":      6,
    "split":            "train"
  }
}
```

---

## Quick Start

```bash
# Install dependencies (Python >= 3.8, no mandatory third-party packages)
pip install -r requirements.txt
```

### 1 · Generate data

```bash
# IID splits
python scripts/generate_single_goal_data.py \
    --out_dir data/single_goal/6x6 --split train    --n_samples 1000 --seed 42

python scripts/generate_single_goal_data.py \
    --out_dir data/single_goal/6x6 --split valid    --n_samples 200  --seed 43

python scripts/generate_single_goal_data.py \
    --out_dir data/single_goal/6x6 --split test_iid --n_samples 200  --seed 44

# OOD split (dense obstacles)
python scripts/generate_single_goal_data.py \
    --out_dir data/single_goal/6x6_dense --split test_ood --n_samples 200 \
    --dense --seed 45
```

All data files are already committed to this repository and do **not** need to be regenerated unless you wish to change the parameters.

### 2 · Preprocess / validate

```bash
python scripts/data_preprocess.py \
    --input  data/single_goal/6x6/train.jsonl \
    --output data/single_goal/6x6/train.jsonl
```

This validates required fields and normalises the `target` action string in-place.

### 3 · Sanity check

```bash
# Check all data files at once
python scripts/sanity_check.py --data_dir data/single_goal

# Or check a single file
python scripts/sanity_check.py --data_file data/single_goal/6x6/test_iid.jsonl
```

Expected output:

```
[✓] data/single_goal/6x6/test_iid.jsonl  n=200  gold_success=1.0000  bad_fail=...  [PASS]
...
All sanity checks passed.
```

The check verifies that:
- **gold paths** always succeed (Success = 1, Feasible = 1)
- **bad actions** (all `up`) almost always fail (fail rate >= 95 %)

### 4 · Evaluate model predictions

Create a predictions JSONL file where each line has:
```json
{"id": "test_iid_000001", "prediction": "right down right down left"}
```

Then run:

```bash
python scripts/evaluate_executor.py \
    --data_file data/single_goal/6x6/test_iid.jsonl \
    --pred_file outputs/predictions.jsonl \
    --out_file  outputs/metrics.json
```

Example output:

```
=== Evaluation Results ===
  Samples evaluated : 200
  ParseRate         : 0.9850
  Feasibility       : 0.9200
  Success Rate      : 0.8750
  Optimality        : 0.8300
```

---

## Metrics

| Metric | Definition |
|---|---|
| **ParseRate** | Fraction of predictions that can be parsed into a valid action sequence |
| **Feasibility** | Fraction of predictions that make no out-of-bounds or obstacle-collision moves |
| **Success Rate** | Fraction of predictions where the agent reaches the goal |
| **Optimality** | Fraction of successful predictions whose length <= gold (shortest) path length |

---

## Reproducibility

All data files included in this repository were generated with fixed seeds:

| Split | Seed | Samples |
|---|---|---|
| train | 42 | 1 000 |
| valid | 43 | 200 |
| test_iid | 44 | 200 |
| test_ood (dense) | 45 | 200 |
