#!/usr/bin/env python3
"""Build the work-card SVGs from the delivered Figma exports.

Run from the repo root:   python3 tools/build-work-svgs.py

Reads `Work Showcases/` (repo root, not served) and writes
`assets/img/works/<slug>.svg`.

WHY THIS EXISTS
---------------
SVG is the right format for these cards and they stay SVG: the frame, the
background fill, the border stroke and the clip paths are all real vector, and
they scale cleanly to any card width.

What is *not* vector is the photograph each one embeds. Figma exports it as a
base64 PNG, and PNG is the worst possible container for a photo — the six
delivered files came to 3.4 MB, of which almost all is one lossless-encoded
photo per file, inflated a further 33% by base64.

So this rewrites only that payload: the embedded raster is re-encoded as JPEG
and spliced back into the same SVG. Nothing about the vector composition
changes; the file is still an SVG and still scales. It just stops shipping a
photo as PNG.

Measured on the delivered set: 3.4 MB -> ~0.6 MB, no visible difference.

TRANSPARENCY
------------
JPEG has no alpha, so a raster that actually uses transparency cannot be
converted without compositing it onto something. Each payload is therefore
tested for real (not merely declared) alpha before conversion — every one of
these declares RGBA, but only Hano_Showcase actually varies it. Anything that
does keeps its PNG payload and is left alone.

Pure stdlib plus macOS `sips`, like the other tools here. No build step, no
project dependency.
"""

import base64
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "Work Showcases")
OUT = os.path.join(ROOT, "assets", "img", "works")
TMP = "/tmp/hano-work-build"

# Delivered name -> the slug index.html already references.
JOBS = {
    "Bybit_Showcase.svg":         "bybit.svg",
    "Kalshi_Showcase.svg":        "kalshi.svg",
    "Maxy_Showcase.svg":          "maxy.svg",
    "LevelsSocials_Showcase.svg": "levels-socials.svg",
    "Crypteum_Showcase.svg":      "the-crypteum.svg",
    "Hano_Showcase.svg":          "hano-crypto.svg",
}

QUALITY = "0.86"
PAYLOAD = re.compile(r'data:image/(png|jpeg);base64,([A-Za-z0-9+/=]+)')


def uses_alpha(png_path):
    """True if the PNG's alpha channel actually varies, not just exists.

    sips is asked for a flattened copy; comparing sizes would be unreliable, so
    the alpha is read directly out of the decoded pixels instead.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "mcl", os.path.join(ROOT, "tools", "make-client-logos.py"))
    mcl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mcl)

    norm = png_path + ".norm.png"
    subprocess.run(["sips", "-s", "format", "png", png_path, "--out", norm],
                   check=True, capture_output=True)
    _, _, px = mcl.read_png(norm)
    # Sample rather than scan: these are ~1MP and a real alpha mask shows up
    # immediately. Step is coprime-ish with the row width to avoid striding
    # down a single column.
    for i in range(3, len(px), 4 * 37):
        if px[i] < 250:
            return True
    return False


def build(src_name, out_name):
    src = os.path.join(SRC, src_name)
    if not os.path.exists(src):
        print("  MISSING  %s" % src_name)
        return False

    svg = open(src, encoding="utf-8", errors="ignore").read()
    m = PAYLOAD.search(svg)
    if not m:
        # No raster at all — pure vector, copy through untouched.
        open(os.path.join(OUT, out_name), "w", encoding="utf-8").write(svg)
        print("  %-20s pure vector, copied" % out_name)
        return True

    kind, b64 = m.group(1), m.group(2)
    before = len(svg)

    os.makedirs(TMP, exist_ok=True)
    stem = os.path.join(TMP, out_name.replace(".svg", ""))
    raw = stem + ".png"
    open(raw, "wb").write(base64.b64decode(b64))

    if kind == "png" and uses_alpha(raw):
        # Real transparency: JPEG would have to composite it onto some colour,
        # which is a visible change. Leave the payload as delivered.
        open(os.path.join(OUT, out_name), "w", encoding="utf-8").write(svg)
        print("  %-20s %4dKB  (alpha in use — PNG payload kept)"
              % (out_name, before // 1024))
        return True

    jpg = stem + ".jpg"
    subprocess.run(["sips", "-s", "format", "jpeg",
                    "-s", "formatOptions", QUALITY, raw, "--out", jpg],
                   check=True, capture_output=True)

    new_b64 = base64.b64encode(open(jpg, "rb").read()).decode("ascii")
    svg = svg[:m.start()] + "data:image/jpeg;base64," + new_b64 + svg[m.end():]

    open(os.path.join(OUT, out_name), "w", encoding="utf-8").write(svg)
    after = len(svg)
    print("  %-20s %4dKB -> %3dKB  (%d%% smaller)"
          % (out_name, before // 1024, after // 1024,
             round((1 - after / before) * 100)))
    return True


def main():
    if not os.path.isdir(SRC):
        sys.exit("no 'Work Showcases/' directory at repo root")
    os.makedirs(OUT, exist_ok=True)
    print("building work card SVGs into assets/img/works/")
    ok = sum(build(s, o) for s, o in JOBS.items())
    print("%d/%d written" % (ok, len(JOBS)))


if __name__ == "__main__":
    main()
