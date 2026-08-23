# Normalized tariff schema

Every file under `data/<org>/normalized/<year>/<date>.json` follows this
common layout, regardless of which organization it came from. This is the
schema new normalizers (see [`CONTRIBUTING.md`](CONTRIBUTING.md)) must
produce.

```jsonc
{
  "schema_version": "1.0",
  "source": {
    "organization": "EKZ (Elektrizitätswerke des Kantons Zürich)",
    "organization_slug": "ekz",
    "country": "CH",
    "api_url": "https://api.tariffs.ekz.ch/v1/tariffs",
    "website": "https://www.ekz.ch",
    "publication_timestamp": "2025-12-18T14:41:44+01:00", // as reported by the source API, if any
    "attribution": "Data sourced from ... archived by Strompreise-Schweiz/ekz (...)"
  },
  "retrieved_at": "2026-08-23T19:52:51+00:00", // UTC, when this repo fetched the data
  "date": "2026-08-23",                        // calendar date these prices apply to
  "timezone": "Europe/Zurich",                 // timezone the interval timestamps are expressed in
  "currency": "CHF",
  "resolution_minutes": 15,
  "intervals": [
    {
      "start": "2026-08-23T00:00:00+02:00",
      "end": "2026-08-23T00:15:00+02:00",
      "components": {
        "electricity":   { "chf_per_kwh": 0.0900, "chf_per_month": 3.00 },
        "grid":          { "chf_per_kwh": 0.1098, "chf_per_month": 0.00 },
        "integrated":    { "chf_per_kwh": 0.1998, "chf_per_month": 3.00 },
        "metering":      { "chf_per_month": 5.00 },
        "regional_fees": { "chf_per_kwh": 0.0016, "chf_per_month": 0.00 }
      },
      "total_chf_per_kwh": 0.1998
    }
    // ... one entry per interval covering the full day
  ]
}
```

Notes:

- `components` keys are whatever cost buckets the source organization
  reports (e.g. `electricity`, `grid`, `metering`, `regional_fees`). Not
  every organization will report the same buckets — treat unknown/missing
  buckets as absent, not zero.
- `total_chf_per_kwh` is each normalizer's best-effort "what a consumer
  actually pays per kWh" figure. Check the normalizer source
  (`scripts/normalizers/<slug>.py`) to see exactly how it's derived for a
  given organization.
- The `raw/` counterpart of each file (`data/<org>/raw/<year>/<date>.json`)
  is the byte-for-byte response from the source API, kept for provenance —
  it does **not** follow this schema.

## Raw files

`data/<org>/raw/<year>/<date>.json` is the untouched response body as
returned by the organization's own API on the day it was fetched. Its shape
is whatever that organization's API defines and can differ completely
between organizations.
