"""Keep Atlas numbering consistent when any writer rebuilds the catalog."""

import json
from pathlib import Path
from stat import S_IMODE
from tempfile import NamedTemporaryFile


def order_catalog(catalog):
    profiles = sorted(catalog["profiles"], key=lambda entry: entry["domain"] != "single_objective")
    return {
        **catalog,
        "selection": "All active profiles, with single-objective profiles first and relative order preserved within both groups.",
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
