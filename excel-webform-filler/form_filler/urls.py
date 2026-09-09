from __future__ import annotations

from urllib.parse import urljoin


def build_form_url(base_url: str, location_path: str, product_slug: str) -> str:
    path = location_path.strip("/")
    return urljoin(base_url.rstrip("/") + "/", f"{path}/{product_slug}.html")


def lookup_product_slug(product_name: str, catalog: dict[str, str]) -> str | None:
    key = " ".join(product_name.upper().split())
    return catalog.get(key)


def lookup_location_path(sheet_name: str, locations: dict[str, str]) -> str | None:
    return locations.get(sheet_name.strip().upper())
