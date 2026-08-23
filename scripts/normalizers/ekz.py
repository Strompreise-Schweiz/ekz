"""Normalizer for the EKZ tariff API (https://api.tariffs.ekz.ch/v1/tariffs).

Raw response shape: {"publication_timestamp": ..., "prices": [
    {"start_timestamp": ..., "end_timestamp": ...,
     "electricity": [{"unit": "CHF_kWh"|"CHF_m", "value": ...}, ...],
     "grid": [...], "integrated": [...], "metering": [...], "regional_fees": [...]}
]}
"""

SCHEMA_VERSION = "1.0"
COMPONENT_KEYS = ("electricity", "grid", "integrated", "metering", "regional_fees")


def _unit_value(components: list, unit: str):
    for c in components:
        if c.get("unit") == unit:
            return c.get("value")
    return None


def normalize(raw: dict, *, org: dict, retrieved_at: str) -> dict:
    prices = raw["prices"]
    date = prices[0]["start_timestamp"][:10]

    intervals = []
    for p in prices:
        components = {}
        for key in COMPONENT_KEYS:
            values = p.get(key, [])
            entry = {}
            per_kwh = _unit_value(values, "CHF_kWh")
            per_month = _unit_value(values, "CHF_m")
            if per_kwh is not None:
                entry["chf_per_kwh"] = per_kwh
            if per_month is not None:
                entry["chf_per_month"] = per_month
            components[key] = entry

        intervals.append({
            "start": p["start_timestamp"],
            "end": p["end_timestamp"],
            "components": components,
            "total_chf_per_kwh": components.get("integrated", {}).get("chf_per_kwh"),
        })

    return {
        "schema_version": SCHEMA_VERSION,
        "source": {
            "organization": org["name"],
            "organization_slug": org["slug"],
            "country": org.get("country", "CH"),
            "api_url": org["api_url"],
            "website": org.get("website"),
            "publication_timestamp": raw.get("publication_timestamp"),
            "attribution": f"Data sourced from {org['name']} ({org.get('website')}), "
                            f"archived by Strompreise-Schweiz/ekz "
                            f"(https://github.com/Strompreise-Schweiz/ekz).",
        },
        "retrieved_at": retrieved_at,
        "date": date,
        "timezone": "Europe/Zurich",
        "currency": "CHF",
        "resolution_minutes": 15,
        "intervals": intervals,
    }
