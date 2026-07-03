"""
claude_summarizer.py — Usa a API da Anthropic (Claude) para transformar o
contexto estruturado de tarefas atrasadas (task_analyzer.build_report_context)
em um resumo executivo em linguagem natural, pronto para Slack/email.

Sem ANTHROPIC_API_KEY configurada, roda em modo dry run e gera um resumo
determinístico local (sem chamar a API) — útil para testes e para rodar o
agente sem custo.
"""

import json
import os
from typing import Any

SYSTEM_PROMPT = (
    "Voce e um assistente de operacoes. Recebe um JSON com tarefas atrasadas "
    "agrupadas por responsavel e escreve um resumo executivo curto (max 200 "
    "palavras), em portugues, direto ao ponto, destacando: quantas tarefas "
    "estao atrasadas, quem tem mais tarefas atrasadas, e as 3 mais criticas "
    "por dias de atraso. Sem enrolação, sem saudação."
)


def _dry_run_summary(context: dict[str, Any]) -> str:
    """Resumo determinístico gerado localmente, sem chamar a API — usado em testes/CI."""
    overdue_count = context["overdue_count"]
    if overdue_count == 0:
        return f"Nenhuma tarefa atrasada em {context['reference_date']}. Tudo em dia."

    by_owner = context["overdue_by_owner"]
    lines = [f"{overdue_count} tarefa(s) atrasada(s) em {context['reference_date']}."]
    for owner, tasks in sorted(by_owner.items(), key=lambda kv: -len(kv[1])):
        lines.append(f"- {owner}: {len(tasks)} atrasada(s), mais critica: '{tasks[0]['task']}' ({tasks[0]['days_late']}d)")
    return "\n".join(lines)


def summarize_overdue_tasks(context: dict[str, Any]) -> dict[str, Any]:
    """
    Gera o resumo executivo. Retorna {"dry_run": bool, "summary": str}.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        return {"dry_run": True, "summary": _dry_run_summary(context)}

    import anthropic

    client = anthropic.Anthropic(api_key=api_key)
    model = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")

    response = client.messages.create(
        model=model,
        max_tokens=400,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": json.dumps(context, ensure_ascii=False)}],
    )
    summary = "".join(block.text for block in response.content if block.type == "text")
    return {"dry_run": False, "summary": summary}
