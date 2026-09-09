"""Serve the local demo website used by the Selenium script."""

from __future__ import annotations

import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO_DIR = ROOT / "demo_site"


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the local quote-form demo site.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if not DEMO_DIR.exists():
        raise SystemExit("Demo site not found. Run: python scripts/generate_sample_data.py")

    class DemoHandler(SimpleHTTPRequestHandler):
        def __init__(self, *handler_args, **handler_kwargs):
            super().__init__(*handler_args, directory=str(DEMO_DIR), **handler_kwargs)

    server = ThreadingHTTPServer((args.host, args.port), DemoHandler)
    print(f"Serving demo site at http://{args.host}:{args.port}")
    print("Keep this terminal open, then run: python main.py")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
