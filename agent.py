#!/usr/bin/env python3
"""
agent.py — Ponto de entrada do claude-ops-agent.

Le um CSV de tarefas, identifica as atrasadas, gera um resumo executivo via
Claude API e envia para Slack e/ou email.

Uso:
    python agent.py --csv data/sample_tasks.csv
    python agent.py --csv data/sample_tasks.csv --email time@empresa.com
"""

import argparse

from app.claude_summarizer import summarize_overdue_tasks
from app.csv_parser import parse_tasks_csv
from app.notifier import send_to_email, send_to_slack
from app.task_analyzer import build_report_context


def run(csv_path: str, email: str | None = None) -> dict:
    tasks = parse_tasks_csv(csv_path)
    context = build_report_context(tasks)
    result = summarize_overdue_tasks(context)

    slack_result = send_to_slack(result["summary"])
    email_result = send_to_email(result["summary"], email) if email else None

    return {
        "context": context,
        "summary": result,
        "slack": slack_result,
        "email": email_result,
    }


def main():
    parser = argparse.ArgumentParser(description="Claude Ops Agent — resumo de tarefas atrasadas")
    parser.add_argument("--csv", required=True, help="Caminho do CSV de tarefas")
    parser.add_argument("--email", help="Email de destino do resumo (opcional)")
    args = parser.parse_args()

    result = run(args.csv, args.email)

    print(f"Tarefas atrasadas: {result['context']['overdue_count']}/{result['context']['total_tasks']}")
    print("\n--- Resumo ---")
    print(result["summary"]["summary"])
    print(f"\n[dry_run={result['summary']['dry_run']}] Slack: {result['slack']}")
    if result["email"]:
        print(f"[dry_run={result['email']['dry_run']}] Email: {result['email']}")


if __name__ == "__main__":
    main()
