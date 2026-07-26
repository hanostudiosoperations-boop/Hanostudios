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
| `works/` | 6 | 1600×1000 | Bybit, Kalshi, Maxy, Levels Socials, The Crypteum, Hano Crypto |
| `showcase/` | 5 | 1080×2340 | vertical phone-screen stills |
| `services/` | 7 | 800×800 | one still per service, shown on row hover |
| `team/` | 2 | 800×1000 | Johannes, Hannah |
| `clients/` | 10 | 440×120 PNG | client logos, transparent background |
| `og-image.jpg` | 1 | 1200×630 | link preview for X / LinkedIn / iMessage |

Export photographic work as JPG at ~80% quality, not PNG — PNG screenshots run 5–10×
larger for no visible gain, and load time is a real conversion cost on mobile.

`tools/make-placeholders.py` regenerates the placeholder set if you ever need it back.

## Notes

- **The three testimonials in `#reviews` are placeholder copy attributed to real
  clients.** They were written to build the section, not sourced from anyone. Swap in
  real, client-approved quotes before this site goes live.
- The horizontal Works scroll, the word-split transition, and the circle wipe are all
  GSAP ScrollTrigger. If GSAP fails to load, those sections degrade to normal scrollable
  layout automatically — nothing becomes unreachable.
- `prefers-reduced-motion` is respected throughout.
- **Contact form needs an endpoint before launch.** It posts to
  `https://formspree.io/f/FORMSPREE_ID` in `index.html`. Create a free form at
  formspree.io and replace `FORMSPREE_ID` with the real ID — that is the only change
  needed. The form validates and confirms in-page with JS, and falls back to a plain
  browser-validated POST without it.
- The services list in the Figma read "AD CAMPAINGS" — corrected to "Ad Campaigns" here.
