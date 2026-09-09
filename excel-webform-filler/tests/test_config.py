from pathlib import Path

import pytest

from form_filler.config import load_config


def test_load_config_requires_locations(tmp_path: Path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        """
spreadsheet: data/leads.xlsx
products:
  DESK LAMP: desk-lamp
locations: {}
""".strip(),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="location"):
        load_config(config_file)
