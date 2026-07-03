import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ.pop("ANTHROPIC_API_KEY", None)

from app.claude_summarizer import summarize_overdue_tasks


def test_summarize_sem_api_key_roda_dry_run():
    context = {
        "reference_date": "2026-07-03",
        "total_tasks": 8,
        "overdue_count": 2,
        "overdue_by_owner": {
            "Ana": [{"task": "Tarefa A", "due_date": "2026-06-20", "days_late": 13}],
            "Bruno": [{"task": "Tarefa B", "due_date": "2026-06-18", "days_late": 15}],
        },
    }
    result = summarize_overdue_tasks(context)

    assert result["dry_run"] is True
    assert "2 tarefa" in result["summary"]
    assert "Bruno" in result["summary"]


def test_summarize_sem_tarefas_atrasadas():
    context = {"reference_date": "2026-07-03", "total_tasks": 5, "overdue_count": 0, "overdue_by_owner": {}}
    result = summarize_overdue_tasks(context)

    assert result["dry_run"] is True
    assert "Nenhuma tarefa atrasada" in result["summary"]
