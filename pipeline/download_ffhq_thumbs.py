"""
Download FFHQ thumbnails (128x128) from Kaggle and extract subset.
"""

import os
import zipfile
import shutil
import random
from pathlib import Path

def download_ffhq_thumbs(output_dir: str = "./pipeline/input", num_images: int = 500):
    """Download FFHQ thumbnails from Kaggle, extract subset."""

    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
    except ImportError:
        print("ERROR: Kaggle library not installed.")
        print("Install with: pip install kaggle")
        return

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    temp_dir = Path("./pipeline/temp_ffhq_thumbs")
    temp_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading FFHQ thumbnails (128x128) from Kaggle...")
    print(f"Will extract {num_images} random images to {output_dir}")
    print()

    try:
        # Initialize Kaggle API
        api = KaggleApi()
        api.authenticate()

        # Download thumbnails dataset
        # FFHQ thumbnails are part of the main FFHQ dataset
        dataset = 'arnaud58/flickrfaceshq-dataset-ffhq'

        print("Step 1: Downloading FFHQ dataset files list...")

        # List files in dataset
        files = api.dataset_list_files(dataset).files

        # Find thumbnail files
        thumb_files = [f for f in files if 'thumbnails128x128' in f.name and f.name.endswith('.png')]

        if not thumb_files:
            print("ERROR: No thumbnail files found in dataset")
            print("Trying alternative: download full thumbnails folder...")

            # Download entire dataset (will be large)
            print(f"Downloading dataset to {temp_dir}...")
            api.dataset_download_files(dataset, path=str(temp_dir), unzip=True)

            # Find thumbnails folder
            thumb_folder = temp_dir / 'thumbnails128x128'
            if not thumb_folder.exists():
                print("ERROR: thumbnails128x128 folder not found after download")
                print("Dataset structure may have changed.")
                return

            # Get all PNG files
            all_thumbs = list(thumb_folder.rglob('*.png'))

        else:
            print(f"Found {len(thumb_files)} thumbnail files")
            # Download individual files (not supported well, download all)
            print(f"Downloading dataset to {temp_dir}...")
            api.dataset_download_files(dataset, path=str(temp_dir), unzip=True)

            thumb_folder = temp_dir / 'thumbnails128x128'
            all_thumbs = list(thumb_folder.rglob('*.png'))

        print(f"\nStep 2: Found {len(all_thumbs)} thumbnails")
        print(f"Selecting {num_images} random images...")

        # Select random subset
        selected = random.sample(all_thumbs, min(num_images, len(all_thumbs)))

        print(f"\nStep 3: Copying {len(selected)} images to {output_dir}...")

        for idx, src in enumerate(selected, 1):
            dst = output_path / f"ffhq_{idx:05d}.jpg"
            shutil.copy2(src, dst)
            if idx % 50 == 0:
                print(f"  Copied {idx}/{len(selected)} images...")

        print(f"\nExtraction complete! {len(selected)} images saved to {output_dir}")

        # Cleanup
        print("\nCleaning up temporary files...")
        shutil.rmtree(temp_dir)
        print("Done!")

    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nMake sure:")
        print("1. Kaggle API token is set at C:\\Users\\Watusi\\.kaggle\\access_token")
        print("2. You have accepted the dataset terms on Kaggle website:")
        print("   https://www.kaggle.com/datasets/arnaud58/flickrfaceshq-dataset-ffhq")


if __name__ == "__main__":
    download_ffhq_thumbs(num_images=500)
