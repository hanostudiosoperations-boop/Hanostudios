# CLAUDE.md — hano.studios

Context for Claude Code working in this repo.

## What this is

Marketing site for Hano Studios, a creative agency working in Web3 / trading / fintech.
Static site: plain HTML, CSS and JS. **No build step, no package.json, no framework.**
Open `index.html` directly, or serve with `python3 -m http.server`.

Do not introduce a bundler, framework or dependency manager unless explicitly asked.

## Files

```
index.html                 landing page, all sections
work/bybit.html            case study (Figma frame 181) — the pattern for the rest
css/styles.css             all styles; tokens in :root at the top
js/main.js                 menu, reveals, counters, galleries, GSAP scroll sequences
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
(horizontal pin ≥701px, plain vertical stack below — gsap.matchMedia tears the
tween down and CSS lays out the stack) → showcase carousel (video, auto-advance) →
circle wipe → services (light) → team (grows out of the white on scroll) → FAQ →
CTA → footer (Aurora purple, frame 173; the deep Nebula stays on the menu overlay)

There is no separate split section any more. The hero title itself is the element
that divides — `.ht-a` / `.ht-b` are the two words and `.hero-square` is the
transition square. Removing the hero pin means rebuilding that sequence.
The hero pin uses `pinSpacing:false` (the square covers the screen at the end, so
reserved spacing was only ever a black void) and the statement pin box is sized by
padding, not 100svh — both were the causes of the recurring "huge gap" reports.

Footer copyright reads "© 2026 Hano **Animations**" (frame 173 — the legal
entity); the wordmark and the menu overlay say Hano **Studios** (frame 183).
This is deliberate, not a typo.

## Every image in assets/img/ is a placeholder

Generated gradients at final dimensions with final filenames. **To swap in real work,
overwrite the file at the same path. No code changes needed.**

| Path | Count | Dimensions |
|---|---|---|
| `assets/img/works/` | 6 | 1600×1000 (16:10) |
| `assets/img/showcase/` | 5 | 1080×2340 (9:19.5) |
| `assets/img/services/` | 7 | 800×800 (1:1) |
| `assets/img/team/` | 2 | 800×1000 (4:5) |
| `assets/img/og-image.jpg` | 1 | 1200×630 |

**`assets/img/clients/` is real, not placeholder.** All ten marks are the client's own
artwork. The eight PNGs are built from `Client Logos/` (repo root) by
`tools/make-client-logos.py` — re-run that after changing anything in there, don't
hand-edit the output. They are tightly cropped, *not* padded to a fixed canvas: the set
mixes wide wordmarks with square roundels, and the CSS caps both width and height so the
two kinds land at the same optical weight.

**Bybit and Maxy are `.svg` and are NOT rebuilt by the tool.** Both needed a fill edited
for a dark ground — Bybit's wordmark was `#15182A`, and Maxy's paths declared no `fill`
at all, which SVG renders as black. Maxy is filled `#F26B21` (client orange, set on its
`.cls-1` class). Editing either source means redoing that by hand.

The grid sits on Void Black, so polarity matters more than format. Adding a logo means
checking it against black, not assuming — the supplied set alone included pure-black
artwork (Algorand), a light mark inside a dark badge on a white page (Abstract), and a
wordmark on a near-black square (Levels Socials). The tool's modes are `keep` /
`whiten` / `dropbg`; its docstring explains which to reach for and why a luminance key
is the wrong tool for the Abstract case.

`Client Logos/` also holds a dozen further real client marks not currently on the site,
plus `Pudgy Penguins Wordmark.png` — an alternative to the roundel that is **not** used,
because its "PENGUINS" half is dark navy and disappears against Void Black.

## Case study pages (`work/`)

`work/bybit.html` (frame 181), `work/kalshi.html` (frame 207) and
`work/hano-crypto.html` (frame 208) are built — copy any of them for the
remaining three. They reuse `css/styles.css` and `js/main.js` wholesale; only
the CASE STUDY block in the CSS and the "Case-study galleries" block in main.js
are specific to them. Everything outside the `<article class="case">` is
byte-identical across all three, so keep it that way when adding a page.

Kalshi differs from Bybit in three ways the frame dictates: no `<h1>` (the lead
paragraph sits alone beside the logo), a single 9:16 clip on `.slide-tall`
rather than a multi-slide strip, and a `.case-ig` "View on Instagram" caption.

Hano Crypto is the longest frame and adds three more: `.case-logo-badge` (its
mark is a filled purple badge, not a wordmark on the ground), `.case-post` +
`.case-metrics` for a viral-post title with its engagement line above its own
clip, and `.slide-board` for the wide 1340x712 mood board. **`.slide-board`
needs `.slide.slide-board` specificity** — as a single class it loses to the
later `.slide img{width:auto;height:100%}` and the slide collapses to 0 high.
It also has no "Why It Matters" section; don't add one.

Hano Crypto has no client-grid logo, and the only supplied artwork is a raster
crop off the mood board whose dark corners showed against Void Black. The mark
at `assets/img/clients/hano-crypto.svg` is rebuilt as vector — each glyph of
HA_O is placed individually so the bar can sit over the N alone (a second text
run collides with the first).
Paths are `../` throughout, and the menu's Work/Process/Team/FAQ links point at
`../index.html#…` so they work from a subdirectory.

**Frame 181 indents the whole document; it is not a two-column grid.** The left
column is a margin holding only the client logo and the "Why It Matters" label —
section headings sit in the copy column, above their own paragraphs, *not* out
in the margin. Only those two rows are grids (`.case-row`); every ordinary
section is a `.case-sec` block pushed across by `--indent`. That variable has to
reproduce the grid's own maths: `.26fr` against `1fr` is **not** 26%, it is
`.26/1.26` of the width less the gap. Treating it as 26% puts every heading 70px
right of the galleries.

Galleries are `[data-gallery]`; main.js wires arrows, dots, swipe and per-slide
video play/pause for any number of them per page. **Slides are capped on both
axes** — a height cap alone makes 16:9 stills ~1.8x the phone's width, a width
cap alone lets the track grow to the tallest slide and strands the arrows
hundreds of px below a short one. `align-items:flex-start` stops flex equalising
their heights.

Videos use `preload="none"`, so nothing downloads for slides never reached — but
that also leaves the element at `readyState 0` with no source selected, and
`play()` on that rejects without ever fetching. main.js calls `load()` first the
one time a slide becomes active. **Playwright's bundled Chromium has no
proprietary codecs** (`canPlayType('video/mp4; codecs="avc1…"')` is empty), so
playback can only be verified with `chromium.launch({channel:'chrome'})` — it
fails there for the existing showcase clips too, which is the browser, not the file.

Source masters live outside the repo: `~/Downloads/bybit` (88MB),
`~/Downloads/Kalshi` (88MB, one 1080x1920 clip) and `~/Downloads/Hano Crypto`
(397MB, two 1080x1920 clips plus the mood board and analytics PNGs). Re-encoded
to 5.4MB, 2.4MB and 7.2MB with the same settings the showcase clips use: H.264,
CRF 27, long edge 960, AAC 96k, `+faststart`. Kalshi's poster is grabbed at
`-ss 3` — the clip opens on near-black, so frame 0 gives a 4.5KB blank; Hano
Crypto ships its own poster JPEGs.

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
