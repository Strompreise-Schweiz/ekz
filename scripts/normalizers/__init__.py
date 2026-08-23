from .ekz import normalize as normalize_ekz

# Maps the "normalizer" key from config/orgs.json to a normalize(raw, org, retrieved_at) callable.
REGISTRY = {
    "ekz": normalize_ekz,
}
