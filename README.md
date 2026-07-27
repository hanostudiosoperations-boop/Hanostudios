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
| `works/` | 6 | 682×430 SVG | **already real** — built from `Work Showcases/`, see below |
| `showcase/` | 5 | 1080×2340 | vertical phone-screen stills |
| `services/` | 7 | 800×800 | one still per service, shown on row hover |
| `team/` | 2 | square | **already real** — built from `Team Photos/`, see below |
| `clients/` | 10 | tightly cropped | **already real** — 8 PNG via `tools/make-client-logos.py`, plus `bybit.svg` / `maxy.svg` |
| `og-image.jpg` | 1 | 1200×630 | link preview for X / LinkedIn / iMessage |

Export photographic work as JPG at ~80% quality, not PNG — PNG screenshots run 5–10×
larger for no visible gain, and load time is a real conversion cost on mobile.

`tools/make-placeholders.py` regenerates the placeholder set if you ever need it back.
It no longer owns `clients/` — those are real marks now; use `tools/make-client-logos.py`,
which reads `Client Logos/` at the repo root. Both are pure stdlib (plus macOS `sips`).

### Work card images

`Work Showcases/` (repo root, **not served**) holds the delivered Figma exports;
`tools/build-work-svgs.py` turns them into `assets/img/works/<slug>.svg`.

**They stay SVG** — the frame, background fill, border stroke and clip paths are real
vector and scale cleanly to any card width. What is *not* vector is the photograph each
one embeds, which Figma writes out as a base64 PNG. PNG is the worst container for a
photo, and base64 adds a further 33%: as delivered the six came to **3.4 MB**, nearly all
of it one lossless-encoded photo per file.

So the tool rewrites only that payload — the embedded raster is re-encoded as JPEG and
spliced back into the same SVG. The vector composition is untouched, the file is still an
SVG, it still scales. **3.4 MB → 368 KB.**

One exception, handled automatically: JPEG has no alpha, so a payload that genuinely uses
transparency can't be converted without compositing it onto something. Each is tested for
*real* (not merely declared) alpha first — all six declare RGBA, but only `Hano_Showcase`
actually varies it, so that one keeps its PNG payload.

To replace one: drop the new SVG in `Work Showcases/`, add it to `JOBS` if the name is
new, re-run the tool. The filenames in `index.html` never change, so no code edit needed.

### Team photos

`Team Photos/` (repo root, **not served**) holds the originals. They are converted to
`assets/img/team/<slug>.jpg` at q86 — 1.6 MB of PNG down to 76 KB, at native resolution
(don't upscale with `sips -Z`; it adds bytes, not detail). Both are square while the card
is 4:5, so `background-size:cover` crops the sides — centred faces survive that, off-centre
ones won't.

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
