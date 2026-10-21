#!/usr/bin/env node
// Render the HVN GROUP logo SVGs in Resources/Brand to transparent PNGs the
// app shows in its header and About window. The PNGs are committed, so the
// macOS build needs neither a browser nor an SVG rasterizer.
//
// Usage: node scripts/render-brand-logos.mjs   (needs the `playwright` package)
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const brand = join(dirname(fileURLToPath(import.meta.url)), '..', 'Resources', 'Brand');
const height = 120; // 5× the 24 pt header height, sharp on Retina displays

const browser = await chromium.launch();
try {
  for (const name of ['hvn-logo-color', 'hvn-logo-white']) {
    const svg = readFileSync(join(brand, `${name}.svg`), 'utf8');
    const [, , viewWidth, viewHeight] = svg.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
    const width = Math.round((height * viewWidth) / viewHeight);
    const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
    await page.setContent(
      `<html><body style="margin:0;background:transparent">` +
        svg.replace('<svg ', `<svg width="${width}" height="${height}" style="display:block" `) +
        `</body></html>`,
    );
    await page.screenshot({ path: join(brand, `${name}.png`), omitBackground: true });
    await page.close();
    console.log(`Wrote Resources/Brand/${name}.png (${width}×${height})`);
  }
} finally {
  await browser.close();
}
