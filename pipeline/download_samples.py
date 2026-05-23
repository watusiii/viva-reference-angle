"""
Download portrait images from Unsplash API.
Uses Unsplash random portrait endpoint for diverse angles.
"""

import urllib.request
import os
import time
from pathlib import Path

def download_samples(output_dir: str = "./pipeline/input", num_samples: int = 150):
    """Download random portrait images from Unsplash."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {num_samples} random portraits from Unsplash to {output_dir}...")
    print("Using Unsplash random API with portrait query...")

    success_count = 0
    for i in range(1, num_samples + 1):
        filename = f"sample_{i:03d}.jpg"
        filepath = output_path / filename

        # Skip if already exists
        if filepath.exists():
            print(f"  [{i}/{num_samples}] {filename} already exists, skipping")
            success_count += 1
            continue

        # Unsplash random API with portrait orientation
        url = f"https://source.unsplash.com/1024x1536/?portrait,face,headshot&sig={i}"

        try:
            print(f"  [{i}/{num_samples}] Downloading {filename}...")
            urllib.request.urlretrieve(url, str(filepath))
            print(f"    OK - Saved")
            success_count += 1
            time.sleep(0.5)  # Rate limit
        except Exception as e:
            print(f"    FAILED: {e}")

    print(f"\nDownload complete! Successfully downloaded: {success_count}/{num_samples}")
    print(f"Check {output_dir}")


if __name__ == "__main__":
    download_samples()
