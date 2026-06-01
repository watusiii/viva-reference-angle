"""
Select 500 random FFHQ thumbnails and copy to input folder.
"""

import random
import shutil
from pathlib import Path

def select_random_thumbs(
    source_dir: str = "./pipeline/temp_ffhq_thumbs",
    output_dir: str = "./pipeline/input",
    num_select: int = 500
):
    """Copy random subset of thumbs to input folder."""

    src_path = Path(source_dir)
    dst_path = Path(output_dir)
    dst_path.mkdir(parents=True, exist_ok=True)

    # Get all PNG files
    all_files = list(src_path.glob("*.png"))

    if not all_files:
        print(f"No PNG files found in {source_dir}")
        return

    print(f"Found {len(all_files)} total images")
    print(f"Selecting {num_select} random images...")

    # Random sample
    selected = random.sample(all_files, min(num_select, len(all_files)))

    print(f"\nCopying {len(selected)} images to {output_dir}...")

    for idx, src in enumerate(selected, 1):
        dst = dst_path / f"ffhq_{idx:05d}.jpg"
        shutil.copy2(src, dst)

        if idx % 50 == 0:
            print(f"  Copied {idx}/{len(selected)}")

    print(f"\nDone! {len(selected)} images in {output_dir}")
    print(f"Original {len(all_files)} images kept in {source_dir}")


if __name__ == "__main__":
    select_random_thumbs()
