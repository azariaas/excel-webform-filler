from __future__ import annotations

import argparse

from form_filler.config import load_config
from form_filler.runner import run


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fill local demo quote forms from an Excel spreadsheet."
    )
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to YAML config (default: config.yaml)",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Read the spreadsheet and print target URLs without opening a browser",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    run(config, validate_only=args.validate_only)


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, KeyError, ValueError) as exc:
        raise SystemExit(f"Error: {exc}") from exc
