import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.csv_parser import parse_tasks_csv
from app.task_analyzer import build_report_context, find_overdue_tasks, group_by_owner

SAMPLE_CSV = Path(__file__).resolve().parents[1] / "data" / "sample_tasks.csv"
REFERENCE_DATE = date(2026, 7, 3)


def test_find_overdue_tasks_ignora_done_e_futuras():
    tasks = parse_tasks_csv(SAMPLE_CSV)
    overdue = find_overdue_tasks(tasks, REFERENCE_DATE)

    overdue_task_names = {t["task"] for t in overdue}
    assert "Fechar folha de pagamento" not in overdue_task_names  # done
    assert "Configurar backup automatico" not in overdue_task_names  # due no futuro
    assert "Migrar banco de dados para novo servidor" in overdue_task_names  # atrasada


def test_find_overdue_tasks_conta_corretamente():
    tasks = parse_tasks_csv(SAMPLE_CSV)
    overdue = find_overdue_tasks(tasks, REFERENCE_DATE)
    assert len(overdue) == 6


def test_group_by_owner_ordena_por_mais_antiga():
    tasks = parse_tasks_csv(SAMPLE_CSV)
    overdue = find_overdue_tasks(tasks, REFERENCE_DATE)
    grouped = group_by_owner(overdue)

    assert "Carla" in grouped
    assert grouped["Carla"][0]["due_date"] == date(2026, 6, 15)


def test_build_report_context_estrutura_completa():
    tasks = parse_tasks_csv(SAMPLE_CSV)
    context = build_report_context(tasks, REFERENCE_DATE)

    assert context["reference_date"] == "2026-07-03"
    assert context["total_tasks"] == 8
    assert context["overdue_count"] == 6
    assert "Carla" in context["overdue_by_owner"]
    assert context["overdue_by_owner"]["Carla"][0]["days_late"] == 18
