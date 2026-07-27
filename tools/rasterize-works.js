/* Rasterise the delivered *_Showcase.svg work cards to JPEG.
 *
 *   node tools/rasterize-works.js
 *
 * Reads `Work Showcases/` (repo root, not served) and writes
 * assets/img/works/<slug>.jpg. The filenames in index.html never change, so
 * swapping artwork needs no code edit.
 *
 * The exports are composed scenes — background fill, a positioned and
 * sometimes mirrored raster, a border — wrapping a base64 PNG, so the
 * embedded raster cannot simply be extracted without losing the composition
 * (LevelsSocials in particular places a portrait 816x922 image, mirrored, into
 * half of a landscape 682x430 frame). The SVG is therefore rendered whole.
 *
 * JPEG because the content is photographic: as delivered the six came to
 * 3.4MB, and at q86 they are 472KB for no visible difference. PNG for photos,
 * then base64'd (+33%), is the worst case for weight.
 *
 * NOTE: this is the one tool here that needs Playwright, which is NOT a
 * project dependency (see CLAUDE.md — the site itself has no build step).
 * It is a rare, one-off conversion; run it with a global/temporary Playwright
 * install. Nothing on the site depends on it at runtime. */
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');

const SRC = require('path').join(__dirname, '..', 'Work Showcases');
const OUT = require('path').join(__dirname, '..', 'assets', 'img', 'works');
const MAP = {
  'Bybit_Showcase.svg':         'bybit.jpg',
  'Kalshi_Showcase.svg':        'kalshi.jpg',
  'Maxy_Showcase.svg':          'maxy.jpg',
  'LevelsSocials_Showcase.svg': 'levels-socials.jpg',
  'Crypteum_Showcase.svg':      'the-crypteum.jpg',
  'Hano_Showcase.svg':          'hano-crypto.jpg',
};
// 2x the 682x430 frame, so the 520px-max card stays sharp on retina.
const W = 1364, H = 860;

(async () => {
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1 })).newPage();
  for (const [svg, out] of Object.entries(MAP)) {
    const src = path.join(SRC, svg);
    if (!fs.existsSync(src)) { console.log('  MISSING ' + svg); continue; }
    const data = fs.readFileSync(src).toString('base64');
    await p.setContent(
      `<style>html,body{margin:0;padding:0;background:#0A0A0A}
       img{display:block;width:${W}px;height:${H}px}</style>
       <img src="data:image/svg+xml;base64,${data}">`);
    await p.waitForTimeout(450);
    const dest = path.join(OUT, out);
    const before = fs.statSync(src).size;
    await p.screenshot({ path: dest, type: 'jpeg', quality: 86 });
    const after = fs.statSync(dest).size;
    console.log(`  ${out.padEnd(20)} ${(before/1024).toFixed(0).padStart(4)}KB svg -> ${(after/1024).toFixed(0).padStart(3)}KB jpg`);
  }
  await b.close();
})();
