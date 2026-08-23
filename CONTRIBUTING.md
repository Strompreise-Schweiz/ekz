# Adding a new organization

This repo archives daily electricity tariff data from utilities that publish
a "static REST API"-style JSON tariff feed. To add a new organization:

1. **Register it** in [`config/orgs.json`](config/orgs.json):

   ```jsonc
   {
     "slug": "example",                              // used as the data/<slug>/ folder name
     "name": "Example Energy AG",
     "country": "CH",
     "api_url": "https://api.tariffs.example.ch/v1/tariffs",
     "website": "https://www.example.ch",
     "normalizer": "example"                          // must match the key you register below
   }
   ```

2. **Write a normalizer** at `scripts/normalizers/<slug>.py` with a
   `normalize(raw: dict, *, org: dict, retrieved_at: str) -> dict` function
   that turns that organization's raw API response into the common schema
   described in [`SCHEMA.md`](SCHEMA.md). Use
   [`scripts/normalizers/ekz.py`](scripts/normalizers/ekz.py) as a template.

3. **Register the normalizer** in
   [`scripts/normalizers/__init__.py`](scripts/normalizers/__init__.py):

   ```python
   from .example import normalize as normalize_example

   REGISTRY = {
       "ekz": normalize_ekz,
       "example": normalize_example,
   }
   ```

4. Run `python3 scripts/fetch_and_normalize.py` locally to verify it
   produces `data/<slug>/raw/<year>/<date>.json` and
   `data/<slug>/normalized/<year>/<date>.json` without errors.

No other code needs to change — the workflow and the fetch script iterate
over every entry in `config/orgs.json` automatically.

## Before adding a source

Check that organization's terms of use for their API. This project only
redistributes tariff data with attribution (see `data/LICENSE`); it's your
responsibility to confirm the source allows that kind of redistribution
before wiring it in.
