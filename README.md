# Hano Studios — website

Static site. No build step, no dependencies to install. Open `index.html` and it runs.

```
index.html
css/styles.css
js/main.js
assets/logo/      your six logo files
assets/img/       drop real project images here
```

## Deploy

Drag the whole folder onto **Netlify Drop** (app.netlify.com/drop) or run `vercel` in this
directory. Both are free and give you HTTPS and a domain in about a minute. Point
`hano.studios` at it from your registrar's DNS afterwards.

## Brand tokens

All colours and type live at the top of `css/styles.css` under `:root`, straight from the
brand guidelines:

| Token | Value | Name |
|---|---|---|
| `--void` | `#0A0A0A` | Void Black |
| `--frost` | `#FFFFFF` | Frost White |
| `--nebula` | `#47127C` | Royal Nebula |
| `--aurora` | `#8B32F7` | Aurora Purple |

Type is Instrument Sans (display + body) with Aleo italic used once, on "dominate markets"
in the hero — matching the guidelines' restraint on the serif.

## Swapping in real images

Every file in `assets/img/` is a generated placeholder sitting at the **final dimensions
with the final filename**, already wired into the page.

**To use real work: overwrite the file at the same path. Nothing in the code changes.**

| Folder | Files | Size | What |
|---|---|---|---|
| `works/` | 6 | 1364×860 | **already real** — rasterised from `Work Showcases/`, see below |
| `showcase/` | 5 | 1080×2340 | vertical phone-screen stills |
| `services/` | 7 | 800×800 | one still per service, shown on row hover |
| `team/` | 2 | 800×1000 | Johannes, Hannah |
| `clients/` | 10 | tightly cropped | **already real** — 8 PNG via `tools/make-client-logos.py`, plus `bybit.svg` / `maxy.svg` |
| `og-image.jpg` | 1 | 1200×630 | link preview for X / LinkedIn / iMessage |

Export photographic work as JPG at ~80% quality, not PNG — PNG screenshots run 5–10×
larger for no visible gain, and load time is a real conversion cost on mobile.

`tools/make-placeholders.py` regenerates the placeholder set if you ever need it back.
It no longer owns `clients/` — those are real marks now; use `tools/make-client-logos.py`,
which reads `Client Logos/` at the repo root. Both are pure stdlib (plus macOS `sips`).

### Work card images

`Work Showcases/` (repo root, **not served**) holds the delivered Figma exports. They are
composed scenes — background fill, a positioned and sometimes mirrored raster, a border —
wrapping a base64 PNG, so the embedded raster cannot simply be pulled out without losing
the composition. They are rendered whole and saved to `assets/img/works/<slug>.jpg`.

That conversion matters: as delivered the six came to **3.4 MB**; rasterised to JPEG at
q86 they are **472 KB**, for no visible difference. Photographic content as PNG, then
base64'd (+33%), is the worst case for weight — the same reason this file says to export
work as JPG.

To replace one: drop the new SVG in `Work Showcases/` and re-render it to the matching
`<slug>.jpg`. The filenames in `index.html` never change, so no code edit is needed.

## Favicons

Generated from `assets/logo/logomark_black.png` by `tools/make-favicons.py` — pure
standard library, no Pillow or ImageMagick needed. Re-run it if the logomark changes:

```
python3 tools/make-favicons.py
```

The mark is centred on a white square rather than stretched, because it is 580×280 and
black — on a transparent ground it would disappear in a dark browser tab. To put it on
brand purple instead, change `BG` at the top of the script and re-run.

## Notes

- **There is no testimonials section.** Figma's menu and footer both list REVIEWS, so
  those links are omitted until real client quotes exist.
- The horizontal Works scroll, the word-split transition, and the circle wipe are all
  GSAP ScrollTrigger. If GSAP fails to load, those sections degrade to normal scrollable
  layout automatically — nothing becomes unreachable.
- `prefers-reduced-motion` is respected throughout.
- **Calendly needs the real scheduling link before launch.** Every "Let's talk" opens a
  booking modal. Replace `CALENDLY_HANDLE` in `index.html` (two places: the embed's
  `data-url` and the `<noscript>` link) with the real URL. The widget script is only
  fetched the first time someone opens the modal, and degrades to a direct booking link
  plus `hello@hano.studios` if it is blocked.
- The services list in the Figma read "AD CAMPAINGS" — corrected to "Ad Campaigns" here.
