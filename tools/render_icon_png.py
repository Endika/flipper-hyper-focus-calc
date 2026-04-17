#!/usr/bin/env python3
"""Render icons/icon.icon to icons/icon.png (10x10 grayscale) — stdlib only."""
import struct
import zlib
from pathlib import Path


def read_icon_grid(path: Path) -> list[list[int]]:
    lines = path.read_text().strip().splitlines()
    if len(lines) < 3:
        raise ValueError("bad icon.icon")
    w, h = map(int, lines[1].split())
    grid = []
    for row in lines[2 : 2 + h]:
        grid.append([int(x) for x in row.split()])
    return grid


def write_png_gray(path: Path, pixels: list[list[int]]) -> None:
    h = len(pixels)
    w = len(pixels[0])
    raw = b""
    for row in pixels:
        raw += b"\0" + bytes(row)

    def chunk(tag: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 0, 0, 0, 0)
    idat = zlib.compress(raw, 9)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")
    path.write_bytes(png)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    icon_in = root / "icons" / "icon.icon"
    icon_out = root / "icons" / "icon.png"
    g = read_icon_grid(icon_in)
    # 0 -> white 255, 1 -> black 0
    px = [[255 if v == 0 else 0 for v in row] for row in g]
    write_png_gray(icon_out, px)
    print(f"Wrote {icon_out}")


if __name__ == "__main__":
    main()
