#!/usr/bin/env python3
"""Download real Pokemon TCG scans for category references (not live offers).

Keeps card artwork intact, scales preserving aspect ratio, and adds only a
transparent margin outside the card. Commercial reuse rights are NOT granted
by the download and must be reviewed by the publisher.
"""
from __future__ import annotations
import hashlib
import io
import json
import time
import urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app" / "assets" / "tcg"
W, H = 1056, 1472
CARDS = (
    ("01-vintage-squirtle-base1-63.png", "Vintage", "Squirtle", "Base Set", "63/102", "https://images.pokemontcg.io/base1/63_hires.png"),
    ("02-illustration-rare-pikachu-173.png", "Illustration Rare", "Pikachu", "Pokemon 151", "173/165", "https://images.pokemontcg.io/sv3pt5/173_hires.png"),
    ("03-double-rare-charizard-ex-006.png", "Double Rare", "Charizard ex", "Pokemon 151", "006/165", "https://images.pokemontcg.io/sv3pt5/6_hires.png"),
)


def download(url: str) -> bytes:
    error = None
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; BlackFridayHunter/1.0)"})
            with urllib.request.urlopen(request, timeout=25) as response:
                data = response.read(8_000_001)
            if len(data) > 8_000_000 or not data.startswith(b"\x89PNG\r\n\x1a\n"):
                raise ValueError("Expected PNG scan under 8 MB")
            return data
        except Exception as exc:
            error = exc
            time.sleep(attempt + 1)
    raise RuntimeError(f"Unable to download approved reference URL {url}: {error}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for filename, category, pokemon, set_name, card_number, source_url in CARDS:
        data = download(source_url)
        image = Image.open(io.BytesIO(data)).convert("RGBA")
        original_size = list(image.size)
        image.thumbnail((924, 1290), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        canvas.alpha_composite(image, ((W - image.width) // 2, (H - image.height) // 2))
        assert canvas.getpixel((0, 0))[3] == 0
        canvas.save(OUT / filename, optimize=True)
        records.append({
            "category": category,
            "pokemon": pokemon,
            "set": set_name,
            "number": card_number,
            "file": f"/app/assets/tcg/{filename}",
            "source_url": source_url,
            "source_sha256": hashlib.sha256(data).hexdigest(),
            "original_px": original_size,
            "export_px": [W, H],
            "source_credit": "images.pokemontcg.io",
            "commercial_reuse_authorized": False,
            "purpose": "Category artwork reference only; NOT a product offer",
        })
        print(f"prepared {category}: {pokemon} {card_number} ({original_size} -> {W}x{H})")
    (OUT / "manifest.json").write_text(
        json.dumps({"assets": records, "commercial_reuse_authorized": False}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
