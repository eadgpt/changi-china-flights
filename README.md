# Changi route maps — shared engine

One engine, one map per country. Datasets live in `data/*.json`; the page code is shared.

- `template_body.html` — the map + panel code (reads a `CFG` dataset)
- `head.html` — styles, fonts, light + dark colours
- `geo.json` — country shapes for the region
- `data/indonesia.json`, `data/vietnam.json` — cities, airports, timetables, regions, camera
- `build.py` — `python3 build.py` builds every dataset; `python3 build.py vietnam` builds one
- outputs: `changi-<country>.html` (online), `changi-<country>-offline.html` (works with no internet), `upload/` (GitHub Pages)

Live: Indonesia https://claude.ai/artifact/HMoP6hptFrwCeM9Wgf2oGe · Vietnam https://claude.ai/artifact/Dvj7VsR8fGu3U7azfAnrTY
China map is still its own folder: ../ChangiChinaFlights

Timetables come from flightsfrom.com, read through the built-in browser (curl and WebFetch get 403).

## Combined map
`python3 build.py` also writes `changi-routes.html` / `changi-routes-offline.html`: all three countries in one page with
China / Indonesia / Vietnam buttons. The engine boots per country (`loadCountry` → `boot(cfg, lines)`), so switching
tears the scene down and rebuilds it. China's data now lives in `data/china.json` too (extracted from the old standalone build).
