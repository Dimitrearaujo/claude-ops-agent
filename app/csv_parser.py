"""
csv_parser.py — Le uma planilha/CSV de tarefas operacionais e normaliza cada
linha para um dict com tipos corretos (data, status), pronto para o
task_analyzer processar.

Formato esperado do CSV:
    task,owner,due_date,status
    Enviar relatorio mensal,Ana,2026-06-25,pending
"""

import csv
from datetime import date, datetime
from pathlib import Path
from typing import Any


def parse_tasks_csv(path: str | Path) -> list[dict[str, Any]]:
    """
    Le o CSV e retorna uma lista de tarefas normalizadas:
    {"task": str, "owner": str, "due_date": date, "status": str}

    Levanta ValueError se uma linha tiver data em formato invalido.
    """
    tasks = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                due_date = datetime.strptime(row["due_date"].strip(), "%Y-%m-%d").date()
            except ValueError as exc:
                raise ValueError(f"Data invalida na linha {row}: {exc}") from exc

            tasks.append(
                {
                    "task": row["task"].strip(),
                    "owner": row["owner"].strip(),
                    "due_date": due_date,
                    "status": row["status"].strip().lower(),
                }
            )
    return tasks
