import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

for key in ("ANTHROPIC_API_KEY", "SLACK_WEBHOOK_URL", "RESEND_API_KEY"):
    os.environ.pop(key, None)

from agent import run

SAMPLE_CSV = Path(__file__).resolve().parents[1] / "data" / "sample_tasks.csv"


def test_run_end_to_end_em_dry_run():
    result = run(str(SAMPLE_CSV))

    assert result["context"]["total_tasks"] == 8
    assert result["summary"]["dry_run"] is True
    assert result["slack"]["dry_run"] is True
    assert result["email"] is None


def test_run_com_email_dispara_dry_run_de_email():
    result = run(str(SAMPLE_CSV), email="time@empresa.com")
    assert result["email"]["dry_run"] is True
