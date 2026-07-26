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

hero (pinned: title rises to centre, divides, square grows to cover) → statement
(pinned: lines reveal one per scroll, then floats and sticks) + clients → works
(horizontal pin) → showcase carousel (video, auto-advance) → circle wipe →
services (light) → team (grows out of the white on scroll) → FAQ → CTA → footer

There is no separate split section any more. The hero title itself is the element
that divides — `.ht-a` / `.ht-b` are the two words and `.hero-square` is the
transition square. Removing the hero pin means rebuilding that sequence.

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

- **No testimonials section.** It was removed because the quotes were invented. Figma
  lists REVIEWS in both the menu overlay and the footer, so both links are currently
  left out — restore the section and both links together once there are real,
  client-approved quotes.
- **Showcase videos are not supplied yet.** Each `.phone` holds a `<video>` with the
  existing still as its `poster`. The playback controller in `main.js` is finished and
  verified: it plays the active slide, auto-advances on `ended`, wraps around, pauses
  off-screen, and the arrows work. It activates per phone the moment you add
  `data-src="assets/video/showcase/<slug>.mp4"` to that `<video>` — there is a comment
  beside each one with the exact line. A phone with no `data-src` just shows its poster,
  so no missing file is ever requested.
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
