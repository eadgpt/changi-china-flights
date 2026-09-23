# Changi route maps — shared engine

One engine, one map per country. Datasets live in `data/*.json`; the page code is shared.

- `template_body.html` — the map + panel code (reads a `CFG` dataset)
- `head.html` — styles, fonts, light + dark colours
- `geo.json` — country shapes for the region
- `data/china.json`, `data/indonesia.json`, `data/vietnam.json` — cities, airports, timetables, regions, camera
- `build.py` — `python3 build.py` builds every dataset plus the combined map; `python3 build.py vietnam` builds one
- outputs: `changi-<country>.html` (online), `changi-<country>-offline.html` (works with no internet), `upload/` (GitHub Pages)
- `archive/ChangiChinaFlights/` — the old standalone China map, kept for reference only

Timetables come from flightsfrom.com, read through a real browser (curl and plain fetches get 403).

## Combined map
`python3 build.py` also writes `index.html` (online) and `changi-routes-offline.html`: all three countries in one page
with China / Indonesia / Vietnam buttons. The engine boots per country (`loadCountry` → `boot(cfg, lines)`), so switching
tears the scene down and rebuilds it.

## Publishing
`upload/` holds the self-contained files for GitHub Pages: `index.html` is the combined map, and each
`changi-<country>.html` is a single-country page. Upload them with `upload/README.md`.
