from __future__ import annotations

from openpyxl import load_workbook

from form_filler.browser import start_driver, submit_quote_form
from form_filler.config import AppConfig
from form_filler.excel_leads import mark_row_processed, read_lead_rows
from form_filler.urls import build_form_url, lookup_location_path, lookup_product_slug


def run(config: AppConfig, *, validate_only: bool = False) -> None:
    if not config.spreadsheet.exists():
        raise FileNotFoundError(
            f"Spreadsheet not found: {config.spreadsheet}. Run scripts/generate_sample_data.py first."
        )

    wb = load_workbook(config.spreadsheet)
    leads, skipped_sheets = read_lead_rows(
        wb,
        config.locations,
        config.header_row,
        config.data_start_row,
        config.processed_fill,
    )

    for sheet_name in skipped_sheets:
            print(f"  skip sheet '{sheet_name}' - no matching location in config")

    if not leads:
        print("No pending rows to process.")
        return

    sent = 0
    errors = 0
    driver = None if validate_only else start_driver(config.browser)

    try:
        for lead in leads:
            slug = lookup_product_slug(lead.product, config.products)
            if not slug:
                print(f"  error: {lead.name} - unknown product '{lead.product}'")
                errors += 1
                continue

            location_path = lookup_location_path(lead.sheet, config.locations)
            url = build_form_url(config.base_url, location_path or "", slug)
            print(f"  {lead.sheet} row {lead.row_number}: {lead.name} -> {url}")

            if validate_only:
                continue

            try:
                submit_quote_form(
                    driver,
                    url,
                    lead,
                    config.browser.wait_seconds,
                    config.browser.pause_after_submit,
                )
                mark_row_processed(wb[lead.sheet], lead.row_number, config.processed_fill)
                wb.save(config.spreadsheet)
                sent += 1
                print(f"    submitted {lead.product} {lead.version}")
            except Exception as exc:
                errors += 1
                print(f"    error: {exc}")
    finally:
        if driver is not None:
            driver.quit()

    if validate_only:
        print(f"Validation finished - {len(leads)} pending rows, {errors} mapping errors.")
    else:
        print(f"Done - {sent} submitted, {errors} errors.")
