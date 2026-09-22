# Changi to China — 3D flight map

Live: https://claude.ai/artifact/Y7iRrUnV52KtUbLisQNWNq

- `body.html` — city list (CITIES array: name, 中文, lon, lat, airport code, airlines, note) + three.js map code
- `head.html` — title, fonts, styles (light + dark colours)
- `geo.json` — country shapes for the region (from world-atlas 50m)
- `changi_wikipedia_source.txt` — Changi Wikipedia page source the 36 cities came from (22 Sep 2026)
- `build.py` — run `python3 build.py` to rebuild `index.html`, then republish
- `ChangiChinaFlights-offline.html` — single file that runs with NO internet (3D library + fonts packed inside, ~1.3 MB). Send this one to people.
- `vendor/` — local copies of three.js 0.147, OrbitControls and the fonts, used to build the offline file
