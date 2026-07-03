"""
task_analyzer.py — Identifica tarefas atrasadas (due_date no passado e
status ainda nao concluido) e agrupa por responsavel, para virar insumo do
resumo gerado pela Claude API.
"""

from collections import defaultdict
from datetime import date
from typing import Any

DONE_STATUSES = {"done", "concluido", "concluída", "completed"}


def find_overdue_tasks(tasks: list[dict[str, Any]], reference_date: date | None = None) -> list[dict[str, Any]]:
    """
    Retorna as tarefas cujo due_date e anterior a reference_date (hoje, por
    padrao) e cujo status ainda nao esta em DONE_STATUSES.
    """
    today = reference_date or date.today()
    return [
        t for t in tasks
        if t["due_date"] < today and t["status"] not in DONE_STATUSES
    ]


def group_by_owner(overdue_tasks: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Agrupa tarefas atrasadas por responsavel, ordenadas pela mais antiga primeiro."""
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for t in overdue_tasks:
        grouped[t["owner"]].append(t)
    for owner in grouped:
        grouped[owner].sort(key=lambda t: t["due_date"])
    return dict(grouped)


def build_report_context(tasks: list[dict[str, Any]], reference_date: date | None = None) -> dict[str, Any]:
    """
    Monta o contexto estruturado (contagens + agrupamento) que sera passado
    para a Claude API gerar o resumo em linguagem natural.
    """
    today = reference_date or date.today()
    overdue = find_overdue_tasks(tasks, today)
    grouped = group_by_owner(overdue)

    return {
        "reference_date": today.isoformat(),
        "total_tasks": len(tasks),
        "overdue_count": len(overdue),
        "overdue_by_owner": {
            owner: [
                {"task": t["task"], "due_date": t["due_date"].isoformat(), "days_late": (today - t["due_date"]).days}
                for t in owner_tasks
            ]
            for owner, owner_tasks in grouped.items()
        },
    }
