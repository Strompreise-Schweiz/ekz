# EKZ (Elektrizitätswerke des Kantons Zürich)

[![VSE 1.0.0](https://img.shields.io/endpoint?url=https%3A%2F%2Fdata.strompreise-schweiz.ch%2Fekz%2Fbadges%2Fvse-1.0.0.json)](data/checks.json)
[![VSE 1.0.1](https://img.shields.io/endpoint?url=https%3A%2F%2Fdata.strompreise-schweiz.ch%2Fekz%2Fbadges%2Fvse-1.0.1.json)](data/checks.json)

The badges show whether the yearly tariff file the utility publishes follows the
[OpenAPI definitions of the VSE](https://github.com/Strompreise-Schweiz/tariff-core/tree/main/schemas/vse). Details in [`data/checks.json`](data/checks.json).

Tariff data of EKZ (Elektrizitätswerke des Kantons Zürich), published by the
[Strompreise Schweiz](https://github.com/Strompreise-Schweiz) initiative. All logic lives in
[`tariff-core`](https://github.com/Strompreise-Schweiz/tariff-core); this repo holds configuration,
corrections and data.

Everything is listed in `https://data.strompreise-schweiz.ch/ekz/index.json`.

## Where what is

| Question | Place | Changed by |
|---|---|---|
| Where does the data come from? | [`config/source.json`](config/source.json) | a person |
| What does a person change? | `curation/<year>.json`, each change with a reason | a person |
| What is wrong with it? | [`data/checks.json`](data/checks.json) | GitHub Actions |
| What is published? | `data/`: `sources/` as the utility sent it, the rest built from it | GitHub Actions |

## Yearly tariff file

| What | Stable URL |
|---|---|
| Current year | `https://data.strompreise-schweiz.ch/ekz/tariffs/current.json` |
| A given year | `https://data.strompreise-schweiz.ch/ekz/tariffs/<year>.json` |

The VSE format (OpenAPI 1.0.1) with additional fields: `tariffs[].id`, `products` (which tariffs
belong together) and `_meta` (sources, repairs and corrections). It holds all three tariff forms:
`constant`, `multilevel` and `dynamic`. For a dynamic tariff, `prices.dynamic.url` points to the day
prices below. Prices exclude VAT.

## Day prices

One file per Swiss calendar day in the format of HDN 2025, chapter 7.4, always in quarter hours.
`latest.json` holds today and, once published, tomorrow. These URLs never change.

**Products**: every component a customer pays per quarter hour (energy, grid, metering, and
`integrated` as the sum per kWh).

| Product | Year | Stable URL |
|---|---|---|
| EKZ Energie Dynamisch + EKZ Netz 400D | 2026 | `https://data.strompreise-schweiz.ch/ekz/products/dynamisch-400d/latest.json` |
| EKZ Energie Dynamisch + EKZ Netz 400D Cluster 1 | 2027 | `https://data.strompreise-schweiz.ch/ekz/products/dynamisch-400d-cluster-1/latest.json` |
| EKZ Energie Dynamisch + EKZ Netz 400D Cluster 2 | 2027 | `https://data.strompreise-schweiz.ch/ekz/products/dynamisch-400d-cluster-2/latest.json` |
| EKZ Energie Dynamisch + EKZ Netz 400D Cluster 3 | 2027 | `https://data.strompreise-schweiz.ch/ekz/products/dynamisch-400d-cluster-3/latest.json` |
| EKZ Energie Dynamisch + EKZ Netz 400D Cluster 4 | 2027 | `https://data.strompreise-schweiz.ch/ekz/products/dynamisch-400d-cluster-4/latest.json` |

**Price sources**: what one API of the utility sends, with the corrections of `curation/`.

| Source | Valid | Stable URL |
|---|---|---|
| EKZ Energie Dynamisch | open | `https://data.strompreise-schweiz.ch/ekz/prices/electricity-dynamic/latest.json` |
| EKZ Netz 400D including fees (2026) | up to 2026-12-31 | `https://data.strompreise-schweiz.ch/ekz/prices/grid-400d/latest.json` |
| EKZ 400D integrated (2026) | up to 2026-12-31 | `https://data.strompreise-schweiz.ch/ekz/prices/integrated-400d/latest.json` |
| EKZ Netz 400D Cluster 1 including fees | from 2027-01-01 | `https://data.strompreise-schweiz.ch/ekz/prices/grid-400d-cluster-1/latest.json` |
| EKZ Netz 400D Cluster 2 including fees | from 2027-01-01 | `https://data.strompreise-schweiz.ch/ekz/prices/grid-400d-cluster-2/latest.json` |
| EKZ Netz 400D Cluster 3 including fees | from 2027-01-01 | `https://data.strompreise-schweiz.ch/ekz/prices/grid-400d-cluster-3/latest.json` |
| EKZ Netz 400D Cluster 4 including fees | from 2027-01-01 | `https://data.strompreise-schweiz.ch/ekz/prices/grid-400d-cluster-4/latest.json` |
| EKZ standard tariff, archive up to November 2026 | open, no longer fetched | `https://data.strompreise-schweiz.ch/ekz/prices/legacy-default/<year>/<date>.json` |

Timestamps are Swiss local time with an offset, for example `2026-11-02T00:00:00+01:00`.
Parse the offset and do not assume 96 intervals: a day has 92 in March and 100 in October.
Check `_meta.complete` before you use a day.

A past day: `https://data.strompreise-schweiz.ch/ekz/<prices|products>/<id>/<year>/<date>.json` for the current year. All years are in git:
`https://raw.githubusercontent.com/Strompreise-Schweiz/ekz/main/data/<prices|products>/<id>/<year>/<date>.json`.

## Grid clusters from 2027

From 2027 the grid tariff 400D has four variants. A cluster is a group of transformer stations with a
similar load pattern, not a region. EKZ assigns each customer for one tariff year and shows the
assignment in myEKZ. EKZ publishes no list, so it cannot be derived from an address or municipality.
Use the product of your cluster.

## Older data

`legacy-default` holds the archive up to November 2026. It was fetched without `tariff_name`, so it
contains the standard tariff with one price per day and not the dynamic 400D tariff. Do not use it as
dynamic data.

Format details: [`SCHEMA.md`](https://github.com/Strompreise-Schweiz/tariff-core/blob/main/SCHEMA.md).

## License

See [`data/LICENSE`](data/LICENSE) for the data and [`LICENSE`](LICENSE) for the code.
