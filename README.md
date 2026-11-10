# EKZ (Elektrizitätswerke des Kantons Zürich)

Tariff data of EKZ (Elektrizitätswerke des Kantons Zürich), published by the
[Strompreise Schweiz](https://github.com/Strompreise-Schweiz) initiative. All logic lives in
[`tariff-core`](https://github.com/Strompreise-Schweiz/tariff-core); this repo holds configuration,
corrections and data.

Everything is listed in `https://raw.githubusercontent.com/Strompreise-Schweiz/ekz/main/data/index.json`.

## Dynamic tariffs

These URLs never change. Each file holds today and, once published, tomorrow.

| Tariff | Valid | Stable URL |
|---|---|---|
| EKZ Energie Dynamisch | now to open | `https://raw.githubusercontent.com/Strompreise-Schweiz/ekz/main/data/dynamic/electricity-dynamic/latest.json` |
| EKZ Netz 400D including fees (2026) | now to 2026-12-31 | `https://raw.githubusercontent.com/Strompreise-Schweiz/ekz/main/data/dynamic/grid-400d/latest.json` |
| EKZ 400D integrated (2026) | now to 2026-12-31 | `https://raw.githubusercontent.com/Strompreise-Schweiz/ekz/main/data/dynamic/integrated-400d/latest.json` |
| EKZ Netz 400D Cluster 1 including fees | 2027-01-01 to open | `https://raw.githubusercontent.com/Strompreise-Schweiz/ekz/main/data/dynamic/grid-400d-cluster-1/latest.json` |
| EKZ Netz 400D Cluster 2 including fees | 2027-01-01 to open | `https://raw.githubusercontent.com/Strompreise-Schweiz/ekz/main/data/dynamic/grid-400d-cluster-2/latest.json` |
| EKZ Netz 400D Cluster 3 including fees | 2027-01-01 to open | `https://raw.githubusercontent.com/Strompreise-Schweiz/ekz/main/data/dynamic/grid-400d-cluster-3/latest.json` |
| EKZ Netz 400D Cluster 4 including fees | 2027-01-01 to open | `https://raw.githubusercontent.com/Strompreise-Schweiz/ekz/main/data/dynamic/grid-400d-cluster-4/latest.json` |

The format is the VSE format (HDN 2025, chapter 7.4) with an additional `_meta` block.
Timestamps are Swiss local time with an offset, for example `2026-11-02T00:00:00+01:00`.
Parse the offset and do not assume 96 intervals: a day has 92 in March and 100 in October.
Check `_meta.days[].complete` and `_meta.valid_to` before you use the data.

Archive per day: `data/dynamic/<id>/{raw,vse,normalized}/<year>/<date>.json`.

### Grid clusters from 2027

From 2027 the grid tariff 400D has four variants. A cluster is a group of transformer stations with a
similar load pattern, not a region. EKZ assigns each customer for one tariff year and shows the
assignment in myEKZ. EKZ publishes no list, so it cannot be derived from an address or municipality.
Use the URL of your cluster together with `electricity-dynamic`.

## Static tariffs (constant, multilevel)

| What | Stable URL |
|---|---|
| Current year | `https://raw.githubusercontent.com/Strompreise-Schweiz/ekz/main/data/tariffs/current.json` |
| A given year | `https://raw.githubusercontent.com/Strompreise-Schweiz/ekz/main/data/tariffs/<year>.json` |

The format is the VSE format (NNMV annex 10, OpenAPI) with additional fields: `tariffs[].id`,
`products` (which tariffs belong together) and `_meta` (source, repairs and corrections).
Prices exclude VAT.

## Older data

`data/dynamic/legacy-default/` holds the archive up to November 2026. It was fetched without
`tariff_name`, so it contains the standard tariff with one price per day and not the dynamic 400D
tariff. Do not use it as dynamic data.

## Structure

| Path | Content | Who changes it |
|---|---|---|
| `config/source.json` | Data sources | Person |
| `curation/<year>.json` | Corrections and product mapping, each with a reason | Person |
| `data/**` | Generated data | GitHub Actions only |

Format details: [`SCHEMA.md`](https://github.com/Strompreise-Schweiz/tariff-core/blob/main/SCHEMA.md).

## License

See [`data/LICENSE`](data/LICENSE) for the data and [`LICENSE`](LICENSE) for the code.
