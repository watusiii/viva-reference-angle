"""
Download sample portrait images for testing.
Uses Unsplash public domain images.
"""

import urllib.request
import os
from pathlib import Path

# Sample Unsplash portrait URLs (1024x resolution, CC0/public domain)
# These are direct download URLs for portrait photos
SAMPLE_URLS = [
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=1024",  # Woman portrait
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1024",  # Man portrait
    "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=1024",  # Woman smiling
    "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=1024",  # Man with beard
    "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=1024",  # Woman close-up
    "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=1024",  # Man looking away
    "https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?w=1024",  # Woman side view
    "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=1024",  # Man side profile
    "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=1024",  # Woman different angle
    "https://images.unsplash.com/photo-1504593811423-6dd665756598?w=1024",  # Man different angle
    "https://images.unsplash.com/photo-1489424731084-a5d8b219a5bb?w=1024",  # Woman profile
    "https://images.unsplash.com/photo-1463453091185-61582044d556?w=1024",  # Man close portrait
    "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=1024",  # Woman angled
    "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=1024",  # Man looking up
    "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=1024",  # Woman looking down
]


def download_samples(output_dir: str = "./pipeline/input", num_samples: int = 15):
    """Download sample portrait images to output directory."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {num_samples} sample portraits to {output_dir}...")

    for i, url in enumerate(SAMPLE_URLS[:num_samples], 1):
        filename = f"sample_{i:03d}.jpg"
        filepath = output_path / filename

        try:
            print(f"  [{i}/{num_samples}] Downloading {filename}...")
            urllib.request.urlretrieve(url, str(filepath))
            print(f"    OK - Saved")
        except Exception as e:
            print(f"    FAILED: {e}")

    print(f"\nDownload complete! Check {output_dir}")


if __name__ == "__main__":
    download_samples()
