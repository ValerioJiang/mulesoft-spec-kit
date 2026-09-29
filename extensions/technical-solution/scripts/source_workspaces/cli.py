"""CLI used by Spec Kit skills to list and resolve application repositories."""

from __future__ import annotations

import argparse
import json
import sys

from adapters import ResolutionError
from registry import list_sources, resolve_explicit_root, resolve_source


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Resolve a configured Spec Kit source workspace.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    listing = subparsers.add_parser("list", help="list configured source selections")
    listing.add_argument("--domain", help="filter by exact domain ID")

    resolving = subparsers.add_parser("resolve", help="resolve one exact source selection")
    resolving.add_argument("selection", nargs="?", help="workspace ID or workspace ID plus catalog path")
    resolving.add_argument("--root", help="explicit repository root; relative paths use the central workspace root")
    resolving.add_argument("--domain", help="required with --root")
    return parser


def main() -> int:
    parser = build_parser()
    arguments = parser.parse_args()
    try:
        if arguments.command == "list":
            result = list_sources(domain=arguments.domain)
        elif arguments.root:
            if arguments.selection:
                parser.error("provide either a configured selection or --root, not both")
            result = resolve_explicit_root(arguments.root, arguments.domain or "")
        else:
            if not arguments.selection:
                parser.error("resolve requires a configured selection or --root")
            result = resolve_source(arguments.selection)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except ResolutionError as error:
        print(f"source resolver: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
