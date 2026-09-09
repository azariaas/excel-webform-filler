from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class BrowserConfig:
    maximized: bool
    wait_seconds: int
    pause_after_submit: float


@dataclass(frozen=True)
class AppConfig:
    project_root: Path
    spreadsheet: Path
    header_row: int
    data_start_row: int
    processed_fill: str
    base_url: str
    locations: dict[str, str]
    products: dict[str, str]
    browser: BrowserConfig


def _resolve(root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (root / path).resolve()


def load_config(config_path: str | Path) -> AppConfig:
    path = Path(config_path).resolve()
    if not path.exists():
        raise FileNotFoundError(
            f"Config file not found: {path}. Copy config.example.yaml to config.yaml."
        )

    with path.open(encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}

    root = path.parent
    browser = raw.get("browser") or {}
    locations = {str(key).strip().upper(): str(value) for key, value in (raw.get("locations") or {}).items()}
    products = {str(key).strip().upper(): str(value) for key, value in (raw.get("products") or {}).items()}

    if not locations:
        raise ValueError("config.yaml must define at least one location")
    if not products:
        raise ValueError("config.yaml must define at least one product")

    return AppConfig(
        project_root=root,
        spreadsheet=_resolve(root, raw.get("spreadsheet", "data/leads.xlsx")),
        header_row=int(raw.get("header_row", 3)),
        data_start_row=int(raw.get("data_start_row", 4)),
        processed_fill=str(raw.get("processed_fill", "FFFF00")).upper().lstrip("#"),
        base_url=str(raw.get("base_url", "http://127.0.0.1:8000")).rstrip("/"),
        locations=locations,
        products=products,
        browser=BrowserConfig(
            maximized=bool(browser.get("maximized", True)),
            wait_seconds=int(browser.get("wait_seconds", 20)),
            pause_after_submit=float(browser.get("pause_after_submit", 2)),
        ),
    )
