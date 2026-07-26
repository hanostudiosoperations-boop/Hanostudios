# CLAUDE.md — hano.studios

Context for Claude Code working in this repo.

## What this is

Marketing site for Hano Studios, a creative agency working in Web3 / trading / fintech.
Static site: plain HTML, CSS and JS. **No build step, no package.json, no framework.**
Open `index.html` directly, or serve with `python3 -m http.server`.

Do not introduce a bundler, framework or dependency manager unless explicitly asked.

## Files

```
index.html                 single page, all sections
css/styles.css             all styles; tokens in :root at the top
js/main.js                 menu, reveals, counters, GSAP scroll sequences
assets/logo/               real brand logos (final, do not replace)
assets/img/                ALL PLACEHOLDER — see below
tools/make-placeholders.py regenerates the placeholder set
tools/make-favicons.py     regenerates the favicon set from the logomark
favicon.ico                root — browsers request this path implicitly
apple-touch-icon.png       root — iOS requests this path implicitly
assets/favicon/            the linked PNG sizes
```

## Brand tokens — do not invent new colours

From the official brand guidelines. Defined in `:root`.

| Token | Hex | Name |
|---|---|---|
| `--void` | `#0A0A0A` | Void Black |
| `--frost` | `#FFFFFF` | Frost White |
| `--nebula` | `#47127C` | Royal Nebula |
| `--aurora` | `#8B32F7` | Aurora Purple |

Type: **Instrument Sans** display + body (letter-spacing -2% to -4.5% on large sizes),
**Aleo** italic used exactly once, on "dominate markets" in the hero. The guidelines call
for restraint on the serif — keep it that way.

Heading pattern throughout is two-tone: `<h2 class="h-split"><strong>Bold lead</strong> light remainder</h2>`.

## Page sections in order

hero → split transition → statement + clients → works (horizontal pin) → showcase
carousel → circle wipe → services (light) → team → FAQ → CTA → footer (purple)

## Every image in assets/img/ is a placeholder

Generated gradients at final dimensions with final filenames. **To swap in real work,
overwrite the file at the same path. No code changes needed.**

| Path | Count | Dimensions |
|---|---|---|
| `assets/img/works/` | 6 | 1600×1000 (16:10) |
| `assets/img/showcase/` | 5 | 1080×2340 (9:19.5) |
| `assets/img/services/` | 7 | 800×800 (1:1) |
| `assets/img/team/` | 2 | 800×1000 (4:5) |
| `assets/img/clients/` | 10 | 440×120 transparent PNG |
| `assets/img/og-image.jpg` | 1 | 1200×630 |

Client logos are text wordmarks standing in for real brand marks. Replace with the actual
logos — Hano has the rights as their client. Do not scrape brand logos from the web.

## Two deliberate resilience behaviours — don't remove them

1. `main.js` adds `.js` to `<html>` on execution. `.reveal` elements are only hidden via
   `.js .reveal`. If `main.js` fails to load, all content stays visible instead of being
   stranded at `opacity:0`.
2. An inline script in `<head>` adds `.no-gsap` when GSAP is unavailable (blocked CDN, ad
   blocker, CSP). CSS then degrades the pinned Works section, the split transition and the
   circle wipe to plain scrollable layout. Without this, the Works section becomes
   completely unreachable for those users.

Both were verified by killing the scripts. Keep them if you refactor.

## Known outstanding work

- **Testimonials are invented copy.** All three quotes, names and titles in `#reviews`
  were written for layout, but they are attributed to real Hano clients (Bybit EU,
  Kalshi, Maxy.co). Shipping them unchanged puts words in a real client's mouth.
  Replace with quotes the client has given and approved. Blocker for launch.
- **The Calendly link is a placeholder.** `#calEmbed`'s `data-url` (and the `<noscript>`
  link beside it) read `CALENDLY_HANDLE`. Replace with the real scheduling URL or the
  modal opens straight into its "could not load" fallback.
- Footer social links point at bare domains; needs the real profile URLs.
- Figma source reads "AD CAMPAINGS" — corrected to "Ad Campaigns" here.
- Plausible is wired in `<head>` with `data-domain="hano.studios"`. It only starts
  recording once the site is added in the Plausible dashboard. Cookieless, so no
  consent banner. A `Booking opened` goal fires from `main.js` when the Calendly
  modal opens — add it as a goal in Plausible to see conversions.

## Conventions

- `prefers-reduced-motion` is respected; preserve it in anything new.
- Keep focus-visible outlines (`--aurora`).
- Responsive breakpoints at 900px and 600px.
- CSS is organised in commented blocks in section order. Add to the matching block rather
  than appending to the end of the file.
