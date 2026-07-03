import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.csv_parser import parse_tasks_csv

SAMPLE_CSV = Path(__file__).resolve().parents[1] / "data" / "sample_tasks.csv"


def test_parse_tasks_csv_retorna_todas_as_linhas():
    tasks = parse_tasks_csv(SAMPLE_CSV)
    assert len(tasks) == 8


def test_parse_tasks_csv_normaliza_tipos():
    tasks = parse_tasks_csv(SAMPLE_CSV)
    first = tasks[0]
    assert first["task"] == "Enviar relatorio mensal para diretoria"
    assert first["owner"] == "Ana"
    assert first["due_date"] == date(2026, 6, 20)
    assert first["status"] == "pending"


def test_parse_tasks_csv_data_invalida_levanta_erro(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("task,owner,due_date,status\nX,Y,not-a-date,pending\n", encoding="utf-8")

    try:
        parse_tasks_csv(bad_csv)
        assert False, "esperava ValueError"
    except ValueError:
        pass
