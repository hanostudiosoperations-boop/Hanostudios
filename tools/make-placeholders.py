#!/usr/bin/env python3
"""Generate branded placeholder assets for hano.studios at final dimensions.
Every file here is meant to be OVERWRITTEN with real artwork.
Keep the filenames identical and no code changes are needed."""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, math, random

BASE = "/home/claude/hano/assets/img"
F_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Brand-derived tone ramps (dark base -> accent), matching css [data-tone]
TONES = {
    "amber":  ((58, 42, 16),  (13, 9, 6),   (36, 25, 6)),
    "green":  ((13, 42, 28),  (5, 13, 9),   (10, 31, 21)),
    "orange": ((58, 28, 8),   (13, 7, 4),   (42, 20, 6)),
    "lilac":  ((42, 36, 64),  (10, 9, 16),  (30, 26, 48)),
    "steel":  ((36, 36, 36),  (11, 11, 11), (26, 26, 26)),
    "purple": ((71, 18, 124), (18, 5, 32),  (42, 13, 71)),
}

def gradient(w, h, tone, seed=0):
    """Diagonal 3-stop gradient with soft radial bloom + grain."""
    a, b, c = TONES[tone]
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        for x in range(0, w, 2):
            t = (x / w * 0.62 + y / h * 0.38)
            if t < 0.62:
                k = t / 0.62
                col = tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))
            else:
                k = (t - 0.62) / 0.38
                col = tuple(int(b[i] + (c[i] - b[i]) * k) for i in range(3))
            px[x, y] = col
            if x + 1 < w:
                px[x + 1, y] = col

    # soft light bloom
    bloom = Image.new("L", (w, h), 0)
    bd = ImageDraw.Draw(bloom)
    rnd = random.Random(seed)
    cx, cy = int(w * rnd.uniform(.55, .8)), int(h * rnd.uniform(.2, .45))
    r = int(min(w, h) * rnd.uniform(.45, .7))
    bd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=90)
    bloom = bloom.filter(ImageFilter.GaussianBlur(radius=min(w, h) // 6))
    img = Image.composite(Image.new("RGB", (w, h), (255, 255, 255)), img, bloom.point(lambda v: v // 3))

    # grain
    noise = Image.effect_noise((w, h), 7).convert("L").point(lambda v: 128 + (v - 128) // 12)
    img = Image.blend(img, Image.merge("RGB", (noise, noise, noise)), 0.05)
    return img

def label(img, title, sub=None, size_ratio=0.058):
    d = ImageDraw.Draw(img)
    w, h = img.size
    fs = max(15, int(h * size_ratio))
    f1 = ImageFont.truetype(F_BOLD, fs)
    pad = int(w * 0.055)
    d.text((pad, h - pad - fs - (fs if sub else 0) - 8), title, font=f1, fill=(255, 255, 255, 235))
    if sub:
        f2 = ImageFont.truetype(F_REG, int(fs * 0.52))
        d.text((pad, h - pad - int(fs * 0.62)), sub, font=f2, fill=(255, 255, 255, 130))
    return img

def save(img, path, q=82):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if path.endswith(".png"):
        img.save(path, optimize=True)
    else:
        img.convert("RGB").save(path, quality=q, optimize=True, progressive=True)
    print(f"  {path.replace('/home/claude/hano/','')}  {os.path.getsize(path)//1024}KB")

# ---------------------------------------------------------------- WORKS 16:10
print("\nWorks cards (1600x1000)")
WORKS = [
    ("bybit",         "Bybit",          "Ad + Social Campaign",   "amber"),
    ("kalshi",        "Kalshi",         "Co-Publishing Campaign", "green"),
    ("maxy",          "Maxy.co",        "Community Growth",       "orange"),
    ("levels-socials","Levels Socials", "Community Growth",       "lilac"),
    ("the-crypteum",  "The Crypteum",   "Brand + Motion",         "steel"),
    ("hano-crypto",   "Hano Crypto",    "Community Growth",       "purple"),
]
for i, (slug, name, tag, tone) in enumerate(WORKS):
    im = gradient(1600, 1000, tone, seed=i)
    label(im, name, tag)
    save(im, f"{BASE}/works/{slug}.jpg")

# ---------------------------------------------------------------- PHONES 9:19.5
print("\nShowcase phones (1080x2340)")
PHONES = [
    ("hano-crypto", "Hano Crypto", "purple"), ("bybit-card", "Bybit Card", "amber"),
    ("kalshi", "Kalshi", "green"), ("the-crypteum", "The Crypteum", "steel"),
    ("maxy", "Maxy.co", "orange"),
]
for i, (slug, name, tone) in enumerate(PHONES):
    im = gradient(1080, 2340, tone, seed=i + 20)
    label(im, name, size_ratio=0.026)
    save(im, f"{BASE}/showcase/{slug}.jpg")

# ---------------------------------------------------------------- SERVICES 1:1
print("\nService previews (800x800)")
SERVICES = [
    ("motion-design","Motion Design","purple"), ("graphic-design","Graphic Design","orange"),
    ("website-design","Website Design","green"), ("launch-leading","Launch Leading","steel"),
    ("social-media","Social Media","lilac"), ("full-marketing","Full Marketing","amber"),
    ("ad-campaigns","Ad Campaigns","purple"),
]
for i, (slug, name, tone) in enumerate(SERVICES):
    im = gradient(800, 800, tone, seed=i + 40)
    label(im, name, size_ratio=0.062)
    save(im, f"{BASE}/services/{slug}.jpg")

# ---------------------------------------------------------------- TEAM 4:5
print("\nTeam photos (800x1000)")
for i, (slug, name, role, tone) in enumerate([
    ("johannes-naaber", "Johannes Naaber", "Co-Founder & Creative Director", "steel"),
    ("hannah-hess",     "Hannah Hess",     "Co-Founder & Head of Operations", "lilac"),
]):
    im = gradient(800, 1000, tone, seed=i + 60)
    d = ImageDraw.Draw(im)
    # neutral silhouette so it reads as a portrait slot
    d.ellipse([310, 300, 490, 480], fill=(255, 255, 255, 22))
    d.ellipse([250, 520, 550, 900], fill=(255, 255, 255, 22))
    label(im, name, role, size_ratio=0.052)
    save(im, f"{BASE}/team/{slug}.jpg")

# ---------------------------------------------------------------- CLIENT LOGOS
print("\nClient logos (440x120, transparent PNG)")
CLIENTS = ["Bybit","Kalshi","Algorand","Pudgy Penguins","Levels Socials",
           "Humanity Protocol","Virtune","Onara","Maxy","Abstract"]
for name in CLIENTS:
    slug = name.lower().replace(" ", "-")
    im = Image.new("RGBA", (440, 120), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    fs = 46 if len(name) < 12 else 34
    f = ImageFont.truetype(F_BOLD, fs)
    bb = d.textbbox((0, 0), name, font=f)
    d.text(((440 - (bb[2] - bb[0])) / 2, (120 - (bb[3] - bb[1])) / 2 - bb[1]),
           name, font=f, fill=(255, 255, 255, 205))
    save(im, f"{BASE}/clients/{slug}.png")

# ---------------------------------------------------------------- OG IMAGE
print("\nSocial share image (1200x630)")
og = gradient(1200, 630, "purple", seed=99)
d = ImageDraw.Draw(og)
f1 = ImageFont.truetype(F_BOLD, 84)
f2 = ImageFont.truetype(F_REG, 30)
d.text((70, 250), "HANO STUDIOS", font=f1, fill=(255, 255, 255))
d.text((74, 360), "Strategy, design, motion and marketing for brands", font=f2, fill=(255, 255, 255, 165))
d.text((74, 400), "ready to launch, scale, and lead.", font=f2, fill=(255, 255, 255, 165))
save(og, f"{BASE}/og-image.jpg", q=88)

print("\nDone.")
