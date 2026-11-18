"""Read-only CLI for the current memory included in Colombo."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .contracts import ContractError
from .retrieval import Reader
from .store import Store, read_json


def main(argv=None):
    default = Path(__file__).resolve().parents[3] / "long_term_memory"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default)
    commands = parser.add_subparsers(dest="command", required=True)
    query = commands.add_parser("query")
    query.add_argument("request", help="JSON object or @request.json")
    args = parser.parse_args(argv)
    try:
        request = (read_json(Path(args.request[1:])) if args.request.startswith("@")
                   else json.loads(args.request))
        if not isinstance(request, dict):
            raise ContractError("Query request must be a JSON object")
        mode = request.pop("mode")
        if mode not in {"overview", "browse", "search", "read", "expand"}:
            raise ContractError("The Colombo memory CLI is read-only")
        result = Reader(Store(args.root)).call(mode, **request)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ContractError, KeyError, ValueError, OSError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
