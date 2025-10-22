import os
import argparse
from pathlib import Path
from shutil import copy2

def split_hepic(raw_dir, list_dir, output_dir):
    raw_dir = Path(raw_dir)
    list_dir = Path(list_dir)
    output_dir = Path(output_dir)

    for split in ["train", "val", "test"]:
        list_file = list_dir / f"{split}.txt"
        if not list_file.exists():
            print(f"⚠️ {list_file} not found, skipping {split}")
            continue

        split_out = output_dir / split
        split_out.mkdir(parents=True, exist_ok=True)

        with open(list_file, "r") as f:
            files = [line.strip() for line in f.readlines()]

        for rel_path in files:
            src = raw_dir / rel_path
            dst = split_out / Path(rel_path).parent.name / Path(rel_path).name
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.exists():
                copy2(src, dst)
            else:
                print(f"⚠️ Missing file: {src}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=str, required=True, help="Path to raw HePIC dataset")
    parser.add_argument("--lists", type=str, required=True, help="Path to folder with train/val/test lists")
    parser.add_argument("--out", type=str, required=True, help="Output folder for split data")
    args = parser.parse_args()

    split_hepic(args.raw, args.lists, args.out)
