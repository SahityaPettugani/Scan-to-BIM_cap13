import os
import argparse
import random
from pathlib import Path
from shutil import copy2

def split_dataset(input_dir, output_dir, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, seed=42):
    random.seed(seed)

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    # make sure output dirs exist
    for split in ["train", "val", "test"]:
        (output_dir / split).mkdir(parents=True, exist_ok=True)

    # each subfolder = one building (e.g., 1_Eremitani, 2_Castello)
    for building_dir in input_dir.iterdir():
        if not building_dir.is_dir():
            continue

        files = list(building_dir.glob("*.txt"))
        random.shuffle(files)

        n = len(files)
        n_train = int(train_ratio * n)
        n_val = int(val_ratio * n)

        split_files = {
            "train": files[:n_train],
            "val": files[n_train:n_train+n_val],
            "test": files[n_train+n_val:]
        }

        for split, fpaths in split_files.items():
            split_out = output_dir / split / building_dir.name
            split_out.mkdir(parents=True, exist_ok=True)
            for f in fpaths:
                copy2(f, split_out / f.name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True, help="Path to raw dataset folder")
    parser.add_argument("--out", type=str, required=True, help="Output folder for split data")
    parser.add_argument("--train_ratio", type=float, default=0.7)
    parser.add_argument("--val_ratio", type=float, default=0.15)
    parser.add_argument("--test_ratio", type=float, default=0.15)
    args = parser.parse_args()

    split_dataset(args.dataset, args.out, args.train_ratio, args.val_ratio, args.test_ratio)
