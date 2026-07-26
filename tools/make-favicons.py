#!/usr/bin/env python3
"""
Generate the favicon set from assets/logo/logomark_black.png.

Pure standard library — no Pillow, no ImageMagick, matching this repo's
no-dependency rule. Run from anywhere:

    python3 tools/make-favicons.py

Writes:
    favicon.ico                        16 + 32 + 48, PNG-compressed entries
    apple-touch-icon.png               180x180
    assets/favicon/favicon-16x16.png
    assets/favicon/favicon-32x32.png
    assets/favicon/favicon-48x48.png
    assets/favicon/icon-192.png
    assets/favicon/icon-512.png
    site.webmanifest

favicon.ico and apple-touch-icon.png sit at the web root on purpose: browsers
and iOS request those two paths implicitly, with or without a <link> tag.

The logomark is 580x280 and bleeds off its edges by design. It is centred on a
square Frost White canvas rather than stretched, so the proportions survive.
White because the source mark is black — on a transparent or dark ground it
would vanish in a dark browser tab.
"""

import os
import struct
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SRC = os.path.join(ROOT, "assets", "logo", "logomark_black.png")
FAV_DIR = os.path.join(ROOT, "assets", "favicon")

BG = (0xFF, 0xFF, 0xFF)          # --frost, so the black mark stays legible
ICO_SIZES = (16, 32, 48)


# ---------------------------------------------------------------- PNG decode

def read_png(path):
    """Decode a non-interlaced 8-bit RGBA PNG to (w, h, bytearray)."""
    data = open(path, "rb").read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG: %s" % path)

    idat = b""
    w = h = None
    i = 8
    while i < len(data):
        (length,) = struct.unpack(">I", data[i:i + 4])
        ctype = data[i + 4:i + 8]
        body = data[i + 8:i + 8 + length]
        if ctype == b"IHDR":
            w, h, depth, color, _, _, interlace = struct.unpack(">IIBBBBB", body)
            if (depth, color, interlace) != (8, 6, 0):
                raise ValueError(
                    "expected 8-bit RGBA non-interlaced, got depth=%d color=%d interlace=%d"
                    % (depth, color, interlace))
        elif ctype == b"IDAT":
            idat += body
        elif ctype == b"IEND":
            break
        i += 12 + length

    raw = zlib.decompress(idat)
    stride = w * 4
    out = bytearray(w * h * 4)
    prev = bytearray(stride)
    pos = 0

    for y in range(h):
        ftype = raw[pos]
        pos += 1
        line = bytearray(raw[pos:pos + stride])
        pos += stride

        # Undo the per-scanline filter (PNG spec section 9.2)
        if ftype == 1:                                     # Sub
            for x in range(4, stride):
                line[x] = (line[x] + line[x - 4]) & 0xFF
        elif ftype == 2:                                   # Up
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 0xFF
        elif ftype == 3:                                   # Average
            for x in range(stride):
                left = line[x - 4] if x >= 4 else 0
                line[x] = (line[x] + ((left + prev[x]) >> 1)) & 0xFF
        elif ftype == 4:                                   # Paeth
            for x in range(stride):
                a = line[x - 4] if x >= 4 else 0
                b = prev[x]
                c = prev[x - 4] if x >= 4 else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pred = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pred) & 0xFF
        elif ftype != 0:
            raise ValueError("bad filter type %d on row %d" % (ftype, y))

        out[y * stride:(y + 1) * stride] = line
        prev = line

    return w, h, out


# ---------------------------------------------------------------- PNG encode

def write_png(path, w, h, pixels):
    """Write 8-bit RGBA pixels as a PNG."""
    stride = w * 4
    raw = bytearray()
    for y in range(h):
        raw.append(0)                                      # filter: None
        raw += pixels[y * stride:(y + 1) * stride]

    def chunk(tag, body):
        return (struct.pack(">I", len(body)) + tag + body +
                struct.pack(">I", zlib.crc32(tag + body) & 0xFFFFFFFF))

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + chunk(b"IEND", b""))

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(png)
    return png


# ---------------------------------------------------------------- processing

# Downsampling averages in linear light, not sRGB. Averaging gamma-encoded
# values darkens and thickens a thin black mark at 16px; this keeps the edges
# true to the original weight.
_TO_LINEAR = [0.0] * 256
for _v in range(256):
    _c = _v / 255.0
    _TO_LINEAR[_v] = _c / 12.92 if _c <= 0.04045 else ((_c + 0.055) / 1.055) ** 2.4


def _to_srgb(x):
    if x <= 0.0:
        return 0
    if x >= 1.0:
        return 255
    s = 12.92 * x if x <= 0.0031308 else 1.055 * (x ** (1 / 2.4)) - 0.055
    return max(0, min(255, int(s * 255.0 + 0.5)))


def flatten_onto_square(w, h, px, bg):
    """Composite RGBA over `bg` and centre it on an opaque square canvas."""
    side = max(w, h)
    off_x = (side - w) // 2
    off_y = (side - h) // 2

    canvas = bytearray(side * side * 4)
    for i in range(0, len(canvas), 4):
        canvas[i:i + 4] = bytes((bg[0], bg[1], bg[2], 255))

    for y in range(h):
        src = y * w * 4
        dst = ((y + off_y) * side + off_x) * 4
        for x in range(w):
            s = src + x * 4
            a = px[s + 3]
            if a == 0:
                continue
            d = dst + x * 4
            if a == 255:
                canvas[d:d + 3] = px[s:s + 3]
            else:                                          # source-over
                ia = 255 - a
                canvas[d] = (px[s] * a + bg[0] * ia) // 255
                canvas[d + 1] = (px[s + 1] * a + bg[1] * ia) // 255
                canvas[d + 2] = (px[s + 2] * a + bg[2] * ia) // 255
    return side, canvas


def resize(side, px, target):
    """Box-filter downsample a square opaque image, averaging in linear light."""
    out = bytearray(target * target * 4)
    scale = side / target

    for ty in range(target):
        y0 = int(ty * scale)
        y1 = max(y0 + 1, int((ty + 1) * scale))
        for tx in range(target):
            x0 = int(tx * scale)
            x1 = max(x0 + 1, int((tx + 1) * scale))

            r = g = b = 0.0
            n = 0
            for sy in range(y0, y1):
                row = sy * side * 4
                for sx in range(x0, x1):
                    s = row + sx * 4
                    r += _TO_LINEAR[px[s]]
                    g += _TO_LINEAR[px[s + 1]]
                    b += _TO_LINEAR[px[s + 2]]
                    n += 1

            d = (ty * target + tx) * 4
            out[d] = _to_srgb(r / n)
            out[d + 1] = _to_srgb(g / n)
            out[d + 2] = _to_srgb(b / n)
            out[d + 3] = 255
    return out


def write_ico(path, entries):
    """Assemble an .ico whose entries are PNG-compressed (universally supported)."""
    header = struct.pack("<HHH", 0, 1, len(entries))
    offset = 6 + 16 * len(entries)

    directory = b""
    for size, png in entries:
        directory += struct.pack(
            "<BBBBHHII",
            size if size < 256 else 0,                     # 0 means 256
            size if size < 256 else 0,
            0, 0, 1, 32,
            len(png), offset)
        offset += len(png)

    with open(path, "wb") as fh:
        fh.write(header + directory + b"".join(png for _, png in entries))


MANIFEST = """{
  "name": "Hano Studios",
  "short_name": "Hano",
  "icons": [
    { "src": "assets/favicon/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "assets/favicon/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "#0A0A0A",
  "background_color": "#0A0A0A",
  "display": "standalone"
}
"""


def main():
    w, h, px = read_png(SRC)
    print("source %s  %dx%d" % (os.path.relpath(SRC, ROOT), w, h))

    side, square = flatten_onto_square(w, h, px, BG)
    print("squared to %dx%d on #%02X%02X%02X" % (side, side, *BG))

    made = []

    # Standalone PNGs
    for size, path in (
        (16, os.path.join(FAV_DIR, "favicon-16x16.png")),
        (32, os.path.join(FAV_DIR, "favicon-32x32.png")),
        (48, os.path.join(FAV_DIR, "favicon-48x48.png")),
        (192, os.path.join(FAV_DIR, "icon-192.png")),
        (512, os.path.join(FAV_DIR, "icon-512.png")),
        (180, os.path.join(ROOT, "apple-touch-icon.png")),
    ):
        write_png(path, size, size, resize(side, square, size))
        made.append(path)

    # Multi-size .ico
    ico_entries = [(s, write_png(os.path.join(FAV_DIR, "_tmp-%d.png" % s),
                                 s, s, resize(side, square, s)))
                   for s in ICO_SIZES]
    write_ico(os.path.join(ROOT, "favicon.ico"), ico_entries)
    for s in ICO_SIZES:
        os.remove(os.path.join(FAV_DIR, "_tmp-%d.png" % s))
    made.append(os.path.join(ROOT, "favicon.ico"))

    with open(os.path.join(ROOT, "site.webmanifest"), "w") as fh:
        fh.write(MANIFEST)
    made.append(os.path.join(ROOT, "site.webmanifest"))

    for p in made:
        print("  %-42s %6d bytes" % (os.path.relpath(p, ROOT), os.path.getsize(p)))


if __name__ == "__main__":
    main()
