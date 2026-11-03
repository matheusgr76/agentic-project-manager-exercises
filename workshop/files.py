"""Read fictional inputs and write local exercise artifacts."""

from __future__ import annotations

import csv
import json
import logging
from pathlib import Path
from typing import Dict, List


LOGGER = logging.getLogger(__name__)


def read_csv(path: Path, required: List[str]) -> List[Dict[str, str]]:
    try:
        with path.open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            columns = reader.fieldnames or []
            missing = set(required) - set(columns)
            if missing:
                raise ValueError(f"{path.name} lacks columns: {sorted(missing)}")
            rows = list(reader)
    except OSError as error:
        LOGGER.error("Could not read %s: %s", path.name, error)
        raise

    if not rows:
        raise ValueError(f"{path.name} has no records")
    LOGGER.info("Read %s records from %s", len(rows), path.name)
    return rows


def read_text(path: Path) -> str:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as error:
        LOGGER.error("Could not read %s: %s", path.name, error)
        raise
    LOGGER.info("Read %s", path.name)
    return content


def write_json(path: Path, value: Dict[str, object]) -> None:
    write_text(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def write_text(path: Path, value: str) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")
    except OSError as error:
        LOGGER.error("Could not write %s: %s", path.name, error)
        raise
    LOGGER.info("Wrote %s", path)
