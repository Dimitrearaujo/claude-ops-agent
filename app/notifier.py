"""
notifier.py — Envia o resumo gerado pela Claude API para Slack (Incoming
Webhook) e/ou email (Resend). Sem as variaveis de ambiente configuradas,
cada canal roda em modo dry run.
"""

import os

import httpx

RESEND_API_URL = "https://api.resend.com/emails"


def send_to_slack(summary: str) -> dict:
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    message = {"text": f":clipboard: *Resumo de tarefas atrasadas*\n{summary}"}

    if not webhook_url:
        return {"dry_run": True, "payload": message}

    response = httpx.post(webhook_url, json=message, timeout=10.0)
    response.raise_for_status()
    return {"dry_run": False, "status_code": response.status_code}


def send_to_email(summary: str, to_email: str) -> dict:
    api_key = os.environ.get("RESEND_API_KEY")
    from_email = os.environ.get("RESEND_FROM_EMAIL", "onboarding@resend.dev")

    payload = {
        "from": from_email,
        "to": [to_email],
        "subject": "Resumo diario — tarefas atrasadas",
        "text": summary,
    }

    if not api_key:
        return {"dry_run": True, "payload": payload}

    response = httpx.post(
        RESEND_API_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        json=payload,
        timeout=10.0,
    )
    response.raise_for_status()
    return {"dry_run": False, "status_code": response.status_code}
