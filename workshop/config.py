"""Fixed values for the fictional, reproducible Acme workshop."""

from datetime import date
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
INPUTS_DIR = REPOSITORY_ROOT / "acme-practice-packet" / "inputs"
MOCK_RETRIEVAL = (
    REPOSITORY_ROOT
    / "chapters"
    / "05-connected-reporting"
    / "mock-issue-retrieval.csv"
)
CASE_MATRIX = (
    REPOSITORY_ROOT / "chapters" / "06-scheduled-reporting" / "case-matrix.csv"
)
OUTPUTS_DIR = REPOSITORY_ROOT / "workshop" / "outputs"
REPORT_DATE = date(2026, 11, 6)
MAX_CAPACITY_AGE_DAYS = 7
TARGET_ISSUE_ID = "GH-41"
TARGET_DECISION_ID = "DEC-12"
TARGET_DECISION_VERSION = "v2"
