# Strompreise Schweiz — tariff archive

A daily archive of electricity tariff data published by Swiss (and
potentially other) utilities, turned into a static, file-based "REST API"
you can query directly via `raw.githubusercontent.com` — no server, no
auth, no rate limits beyond GitHub's own.

A [GitHub Actions workflow](.github/workflows/fetch-tariffs.yml) runs once a
day (17:30 UTC, i.e. always after 18:00 in Europe/Zurich) and commits a
snapshot of each configured organization's tariff API response.

## Usage

Each day and organization produces two files:

```
data/<org-slug>/raw/<year>/<date>.json          # untouched API response
data/<org-slug>/normalized/<year>/<date>.json   # common schema, see SCHEMA.md
```

For example, today's normalized EKZ tariffs:

```
https://raw.githubusercontent.com/Strompreise-Schweiz/ekz/main/data/ekz/normalized/2026/2026-08-23.json
```

Swap the date/org to fetch any other day or organization once it's added.
See [`SCHEMA.md`](SCHEMA.md) for the exact JSON layout of the normalized
files, and [`CONTRIBUTING.md`](CONTRIBUTING.md) for how to add a new
organization.

## Currently archived

| Organization | Slug | Source API |
|---|---|---|
| EKZ (Elektrizitätswerke des Kantons Zürich) | `ekz` | `https://api.tariffs.ekz.ch/v1/tariffs` |

## Why both raw and normalized?

- `raw/` is kept byte-for-byte as returned by the source, for provenance —
  if you ever need to verify what the organization actually published on a
  given day, this is it.
- `normalized/` maps every organization's data into one common schema so you
  can consume multiple organizations with the same parsing code.

## License

This repository is dual-licensed:

- **Code** (everything outside `data/`) — [MIT](LICENSE).
- **Data** (`data/**`) — [Creative Commons Attribution 4.0](data/LICENSE)
  (CC BY 4.0). You're free to use, share, and build on the data, including
  commercially, as long as you credit both the original data source (named
  in each file's `source` field) and this repository. Each normalized JSON
  file carries its own `source.attribution` string for exactly this reason.

The underlying tariff data belongs to the respective utilities (e.g. EKZ);
this project only archives and redistributes their public API output with
attribution. It is not affiliated with, and not endorsed by, any of the
listed organizations.

## Running it yourself

```bash
python3 scripts/fetch_and_normalize.py
```

Stdlib-only, no dependencies to install. Reads every entry in
[`config/orgs.json`](config/orgs.json) and writes into `data/`.
