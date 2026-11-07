"""Keep one current local investigation and its changed prior versions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict


def update_register(path: Path, result: Dict[str, object]) -> None:
    """Write a keyed result, retain changed history, and verify the readback."""
    register: Dict[str, object] = {}
    if path.exists():
        try:
            register = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError("Cannot read local exception register") from error
    exception_id = str(result["exception_id"])
    previous = register.get(exception_id)
    history = []
    if isinstance(previous, dict):
        history = list(previous.get("history", []))
        prior_result = {key: value for key, value in previous.items() if key != "history"}
        if prior_result != result:
            history.append(prior_result)
    register[exception_id] = {**result, "history": history}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(register, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    try:
        saved = json.loads(path.read_text(encoding="utf-8"))[exception_id]
    except (OSError, json.JSONDecodeError, KeyError) as error:
        raise ValueError("Cannot verify local exception register") from error
    for field in ("exception_id", "evidence_references", "classification"):
        if saved.get(field) != result[field]:
            raise ValueError(f"Exception register readback mismatch: {field}")
