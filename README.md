# Neon Stack 3D

A neon 3D falling-block puzzle that installs as an app and runs with no network.
Three.js WebGL playfield, camera orbit/zoom, animated line-clear explosions, a
synthesized 8-bit soundtrack, and modern stacking rules.

**Live:** <https://neon.robs.ws>

## Play

Two builds ship in this repo:

| Path | What it is |
| --- | --- |
| `/` (`index.html`) | Installable PWA. Vendored Three.js, works fully offline. |
| `/standalone/neon-blocks.html` | Single-file version for sharing. Loads Three.js from a CDN, so it needs a connection the first time. |

## Controls

| Key | Action |
| --- | --- |
| `←` `→` | Move one column |
| `↓` | Soft drop (repeats while held) |
| `↑` / `X` | Rotate clockwise |
| `Z` / `Ctrl` | Rotate counter-clockwise |
| `Space` | Hard drop |
| `C` / `Shift` | Hold |
| `P` / `Esc` | Pause |
| `M` | Music on/off |
| `N` | Sound effects on/off |
| `A` | About |

One key press is one action — no key-repeat acceleration on movement. Soft drop is the
only input that repeats while held.

## Rules

7-bag randomizer, SRS rotation with wall kicks, lock delay with move reset, hold slot,
ghost piece, and T-spin / back-to-back / combo scoring. Line clears are scored as
`QUAD` rather than by the trademarked term.

## Run it locally

```bash
npm run serve        # or: python3 tools/serve.py
# open http://localhost:8766/
```

Open it once with the server running so the service worker can cache the game. After
that you can stop the server, go offline, and reload — it still plays.

## Install

- **Chrome / Edge (desktop & Android):** use the `INSTALL` chip in the top bar, or the
  install icon in the address bar.
- **iOS / iPadOS Safari:** tap `INSTALL` (or Share) → **Add to Home Screen**.
- **Already installed:** it launches standalone, with no browser chrome.

## Offline model

`sw.js` precaches the entire app on first load (HTML, manifest, icons, and the vendored
copy of Three.js r169). Navigation falls back to the cached `index.html`, so the game
boots instantly with no connection.

Bump `CACHE` in `sw.js` whenever you ship changes to `index.html` or `vendor/` — the
new worker deletes the old cache on activate.

## Deploy

Service workers require HTTPS (or `localhost`). This folder is a complete static
deployment: `index.html` at the site root, no build step, no server code.

### Vercel

Production is <https://neon.robs.ws>, served from this repo. Pushes to `main` deploy
automatically through the Vercel Git integration, so a commit is a release.

The CLI is also pinned as a dev dependency, for manual deploys and previews:

```bash
npm install          # once
npm run deploy       # vercel deploy --prod
npm run deploy:preview
```

Or import the repo at vercel.com — framework preset **Other**, no build command, no
output directory.

`vercel.json` pins that explicitly (`framework`, `buildCommand`, `installCommand` and
`outputDirectory` are all `null`) and sets the two headers that matter: `sw.js` and
`index.html` are served with `max-age=0, must-revalidate` so a new deploy is picked up
on the next load instead of being masked by a cached service worker, and the manifest
is served as `application/manifest+json`.

`.vercelignore` keeps `node_modules/`, `package.json`, `package-lock.json`, `tools/`
and this README out of the upload, so the deployment is purely the static site.

After the first deploy, load the URL once, then hard-reload so the worker activates,
then confirm the `INSTALL` chip appears.

Any other static host works the same way — GitHub Pages, Netlify, Cloudflare Pages,
S3/CloudFront. All paths in the manifest and service worker are relative, so the app
also runs from a subpath like `example.com/neon/`.

## Metadata and link previews

Search, social and AI crawlers never run JavaScript, so everything they need is static in
the document head of `index.html`.

- **SEO** — descriptive `<title>` and `<meta name="description">`, `canonical`,
  `robots` with `max-image-preview:large`, plus `sitemap.xml` and `robots.txt`.
- **Open Graph / Twitter** — `og:*` and `twitter:*` tags, `summary_large_image`, and a
  1200×630 card at `icons/og-image.png` declared with explicit width, height, type and
  alt text. Regenerate it with `python3 tools/make_og.py` after editing the copy in it.
  Name changes to the card should also update `og:image:alt`.
- **Entity / GEO** — a JSON-LD `@graph` tying the page to `rob.cr` (author) and
  `talacha.dev` (publisher), plus `rel="me"` links, so search and answer engines can
  resolve who made it. `llms.txt` is a short machine-readable summary of the project,
  written to keep AI answers accurate — including what *not* to claim (no benchmarks
  were run).
- **Provenance** — `<meta name="generator">` records the harness and model that produced
  the build.

Probe the whole set the way a crawler would, with no JS:

```bash
curl -s -A "facebookexternalhit/1.1" https://neon.robs.ws/ \
  | grep -o '<meta \(property\|name\)="\(og\|twitter\):[^>]*>'
```

Sharing the site should unfurl with the card image, the title **Neon Stack 3D**, and a
one-line description. Slack, Discord, iMessage and X cache aggressively — if a change
does not appear, append a query string or use each platform's debugger to re-scrape.

## Layout

```
index.html                        game + install/offline bootstrap
manifest.webmanifest              name, icons, standalone display
sw.js                             precache + offline routing
vercel.json                       static hosting config + headers
package.json                      npm scripts (serve, icons, deploy)
robots.txt                        crawler policy
sitemap.xml                       single-URL sitemap
llms.txt                          site summary for search / AI answer engines
icons/                            generated app icons (any + maskable + iOS) + OG card
vendor/                           Three.js r169 (module + addons used by the game)
standalone/neon-blocks.html       single-file build (CDN Three.js)
tools/serve.py                    local server with correct MIME types
tools/make_icons.py               regenerate icons
tools/make_og.py                  regenerate the 1200x630 social card
```

## Naming

The game is **Neon Stack 3D**. "Tetris" is a registered trademark of Tetris Holding,
LLC, and the name is actively enforced, so it does not appear in the app name, icon,
manifest, or any marketing copy. The mechanics themselves (7-bag, SRS, lock delay,
T-spins, B2B, combos) are not trademarked. The soundtrack and all artwork are generated
for this project.

## Credits

- [talacha.dev](https://talacha.dev)
- [robs.ws](https://robs.ws)
- [rob.cr](https://rob.cr)

Built autonomously in one shot by a coding harness running DeepSeek V4.1 Flash Free
inside OpenCode.
