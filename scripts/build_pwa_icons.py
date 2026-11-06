#!/usr/bin/env python3
"""Generate installable PWA icons from the EXISTING approved Magikarp artwork.

Never redraw or change the mascot. The maskable variants add a white safe zone
around the original icon to prevent Android launchers clipping the character.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
APP=ROOT/"app"
SOURCE=APP/"icon-512.png"

def make() -> None:
    with Image.open(SOURCE) as source:
        master=source.convert("RGBA")
        assert master.size==(512,512), f"Unexpected original icon dimensions: {master.size}"
        for size in (192,512):
            canvas=Image.new("RGBA",(size,size),(255,255,255,255))
            diameter=round(size*0.76)
            original=master.resize((diameter,diameter),Image.Resampling.LANCZOS)
            offset=(size-diameter)//2
            canvas.alpha_composite(original,(offset,offset))
            dest=APP/f"icon-maskable-{size}.png"
            canvas.convert("RGB").save(dest,"PNG",optimize=True)
            print(f"Created {dest.relative_to(ROOT)} from untouched Magikarp source")
        original=master.resize((180,180),Image.Resampling.LANCZOS)
        (APP/"apple-touch-icon.png").write_bytes(b"") if False else None
        original.convert("RGB").save(APP/"apple-touch-icon.png","PNG",optimize=True)
        print("Created app/apple-touch-icon.png")

if __name__=="__main__":
    make()
