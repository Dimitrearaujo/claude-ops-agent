import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ.pop("SLACK_WEBHOOK_URL", None)
os.environ.pop("RESEND_API_KEY", None)

from app.notifier import send_to_email, send_to_slack


def test_send_to_slack_sem_webhook_roda_dry_run():
    result = send_to_slack("resumo de teste")
    assert result["dry_run"] is True
    assert "resumo de teste" in result["payload"]["text"]


def test_send_to_email_sem_api_key_roda_dry_run():
    result = send_to_email("resumo de teste", "time@empresa.com")
    assert result["dry_run"] is True
    assert result["payload"]["to"] == ["time@empresa.com"]
    assert result["payload"]["text"] == "resumo de teste"
