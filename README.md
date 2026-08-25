# EKZ tariff archive

A daily archive of EKZ's dynamic electricity tariff data, turned into a
static, file-based "REST API" you can query directly via
`raw.githubusercontent.com` — no server, no auth, no rate limits beyond
GitHub's own.

Part of the [Strompreise Schweiz](https://github.com/Strompreise-Schweiz)
initiative. The actual fetch/normalize logic lives centrally in
[`tariff-etl`](https://github.com/Strompreise-Schweiz/tariff-etl) — this repo
just holds [`config/source.json`](config/source.json) plus the archived
data. See tariff-etl's [`SCHEMA.md`](https://github.com/Strompreise-Schweiz/tariff-etl/blob/main/SCHEMA.md)
for the exact file layout and JSON schema.

A [GitHub Actions workflow](.github/workflows/fetch-tariffs.yml) runs once a
day (17:30 UTC, i.e. always after 18:00 in Europe/Zurich) and commits a
fresh snapshot.

## Usage

```
data/dynamic/raw/<year>/<date>.json          # untouched EKZ API response
data/dynamic/vse/<year>/<date>.json          # same data, Swiss local time
data/dynamic/normalized/<year>/<date>.json   # common cross-org schema
```

For example, today's normalized tariffs:

```
https://raw.githubusercontent.com/Strompreise-Schweiz/ekz/main/data/dynamic/normalized/2026/2026-08-25.json
```

Swap the date to fetch any other day.

## License

This repository is dual-licensed:

- **Code** (everything outside `data/`) — [MIT](LICENSE).
- **Data** (`data/**`) — [Creative Commons Attribution 4.0](data/LICENSE)
  (CC BY 4.0). You're free to use, share, and build on the data, including
  commercially, as long as you credit both EKZ (the original data source)
  and this repository. Each normalized JSON file carries its own
  `source.attribution` string for exactly this reason.

This project archives and redistributes EKZ's public API output with
attribution. It is not affiliated with, and not endorsed by, EKZ.

## Running it yourself

```bash
python3 /path/to/tariff-etl/engine/fetch_and_normalize.py
```

Run from within this repo's root (needs `config/source.json`, which is
already here). Stdlib-only, no dependencies to install.
