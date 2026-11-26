"""Keep Atlas numbering consistent when any writer rebuilds the catalog."""

import json
from pathlib import Path
from stat import S_IMODE
from tempfile import NamedTemporaryFile


def order_catalog(catalog):
    # Catalog domains are the same primary-task families used by both maps.
    # Preserve the existing family order and each family's internal order so
    # regrouping changes display ordinals without changing research identities.
    families = dict.fromkeys(entry["domain"] for entry in catalog["profiles"])
    family_order = {"single_objective": 0}
    family_order.update((family, index) for index, family in enumerate(
        (family for family in families if family != "single_objective"), 1))
    profiles = sorted(catalog["profiles"], key=lambda entry: family_order[entry["domain"]])
    return {
        **catalog,
        "selection": "All active profiles grouped into contiguous primary-task families, with single-objective profiles first. Other families retain their first-appearance order; relative order is preserved within each family.",
        "profiles": [dict(entry, order=number) for number, entry in enumerate(profiles, 1)],
    }


def load_ordered_catalog(path):
    original = json.loads(path.read_text(encoding="utf-8"))
    ordered = order_catalog(original)
    if ordered != original:
        # Scout can refresh the catalog before invoking the native builder.
        # Keep the on-disk order in sync with the page and graph ordinals.
        write_catalog(path, ordered)
    return ordered


def write_catalog(path, catalog):
    temporary = None
    try:
        with NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(catalog, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        if path.exists():
            temporary.chmod(S_IMODE(path.stat().st_mode))
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
