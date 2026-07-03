# Claude Ops Agent

[![CI](https://github.com/Dimitrearaujo/claude-ops-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Dimitrearaujo/claude-ops-agent/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Anthropic](https://img.shields.io/badge/Claude-Sonnet%204.6-black)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Agente Python que usa a **API da Anthropic (Claude)** para resolver uma tarefa concreta de operações: ler uma planilha de tarefas, identificar o que está atrasado, e gerar um resumo executivo pronto para Slack ou email — **Claude em produção, não em demo**.

## O que ele faz

```
CSV de tarefas (task, owner, due_date, status)
        │
Identifica atrasadas (due_date passado + status != done)
        │
Agrupa por responsável, calcula dias de atraso
        │
Claude gera resumo executivo em linguagem natural
        │
   ┌────┴────┐
 Slack      Email (Resend)
```

## Quick Start

```bash
git clone https://github.com/Dimitrearaujo/claude-ops-agent.git
cd claude-ops-agent
pip install -r requirements.txt
cp .env.example .env  # configure ANTHROPIC_API_KEY + Slack/Resend

python agent.py --csv data/sample_tasks.csv
python agent.py --csv data/sample_tasks.csv --email time@empresa.com
```

Sem `ANTHROPIC_API_KEY` / `SLACK_WEBHOOK_URL` / `RESEND_API_KEY` configurados, cada etapa roda em **modo dry run**: o resumo é gerado localmente (determinístico) e o payload de Slack/email é retornado sem ser enviado — dá pra testar o pipeline inteiro sem custo de API.

## Exemplo de saída

```
Tarefas atrasadas: 6/8

--- Resumo ---
6 tarefa(s) atrasada(s) em 2026-07-03.
- Ana: 2 atrasada(s), mais critica: 'Enviar relatorio mensal para diretoria' (13d)
- Carla: 2 atrasada(s), mais critica: 'Migrar banco de dados para novo servidor' (18d)
- Bruno: 1 atrasada(s), mais critica: 'Revisar proposta comercial cliente Y' (15d)
- Diego: 1 atrasada(s), mais critica: 'Treinar equipe no novo sistema' (23d)

[dry_run=True] Slack: {'dry_run': True, 'payload': {...}}
```

Com `ANTHROPIC_API_KEY` configurada, o mesmo resumo é escrito pelo Claude a partir do contexto estruturado — mais natural e adaptável a qualquer volume de tarefas.

## Estrutura

```
claude-ops-agent/
├── agent.py                    <- Orquestra o pipeline (CLI)
├── app/
│   ├── csv_parser.py           <- Le e normaliza o CSV de tarefas
│   ├── task_analyzer.py        <- Identifica atrasadas + agrupa por owner
│   ├── claude_summarizer.py    <- Chama a API da Anthropic (ou dry run)
│   └── notifier.py             <- Envia para Slack / Resend
├── data/
│   └── sample_tasks.csv        <- Dados de exemplo
└── .env.example
```

## Por que isso resolve uma lacuna real

Vagas de "agentic AI" pedem cada vez mais um agente que **faz algo de verdade com dados operacionais reais** — não só responde perguntas em um chat. Esse repo mostra o padrão mínimo viável: entrada estruturada (CSV, mas poderia ser uma planilha do Google, um banco, um Jira export) → lógica determinística em Python (o que é atrasado, por quanto tempo) → Claude só para a parte que exige linguagem natural (o resumo) → saída em um canal real (Slack/email).

## Testes

```bash
pytest tests/ -v
```

Cobre: parsing de CSV (incluindo data inválida), lógica de atraso (ignora tarefas concluídas e futuras), agrupamento por responsável, resumo em modo dry run (com e sem tarefas atrasadas), notificação Slack/email em dry run, e o pipeline `agent.run()` de ponta a ponta.

## Licença

MIT — use livremente em produção.

---

<details>
<summary>🇺🇸 English</summary>

# Claude Ops Agent

[![CI](https://github.com/Dimitrearaujo/claude-ops-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Dimitrearaujo/claude-ops-agent/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Anthropic](https://img.shields.io/badge/Claude-Sonnet%204.6-black)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A Python agent that uses the **Anthropic API (Claude)** to solve a concrete operations task: read a spreadsheet of tasks, identify what's overdue, and generate an executive summary ready for Slack or email — **Claude in production, not a demo**.

## What it does

```
Task CSV (task, owner, due_date, status)
        │
Identifies overdue items (due_date passed + status != done)
        │
Groups by owner, calculates days late
        │
Claude generates an executive summary in natural language
        │
   ┌────┴────┐
 Slack      Email (Resend)
```

## Quick Start

```bash
git clone https://github.com/Dimitrearaujo/claude-ops-agent.git
cd claude-ops-agent
pip install -r requirements.txt
cp .env.example .env  # configure ANTHROPIC_API_KEY + Slack/Resend

python agent.py --csv data/sample_tasks.csv
python agent.py --csv data/sample_tasks.csv --email team@company.com
```

Without `ANTHROPIC_API_KEY` / `SLACK_WEBHOOK_URL` / `RESEND_API_KEY` configured, every step runs in **dry run mode**: the summary is generated locally (deterministic) and the Slack/email payload is returned without being sent — lets you test the whole pipeline with zero API cost.

## Sample output

```
Overdue tasks: 6/8

--- Summary ---
6 task(s) overdue as of 2026-07-03.
- Ana: 2 overdue, most critical: 'Send monthly report to the board' (13d)
- Carla: 2 overdue, most critical: 'Migrate database to new server' (18d)
- Bruno: 1 overdue, most critical: 'Review commercial proposal for client Y' (15d)
- Diego: 1 overdue, most critical: 'Train team on the new system' (23d)

[dry_run=True] Slack: {'dry_run': True, 'payload': {...}}
```

With `ANTHROPIC_API_KEY` configured, the same summary is written by Claude from the structured context — more natural and adaptable to any volume of tasks.

## Structure

```
claude-ops-agent/
├── agent.py                    <- Orchestrates the pipeline (CLI)
├── app/
│   ├── csv_parser.py           <- Reads and normalizes the task CSV
│   ├── task_analyzer.py        <- Identifies overdue items + groups by owner
│   ├── claude_summarizer.py    <- Calls the Anthropic API (or dry run)
│   └── notifier.py             <- Sends to Slack / Resend
├── data/
│   └── sample_tasks.csv        <- Sample data
└── .env.example
```

## Why this fills a real gap

"Agentic AI" job postings increasingly ask for an agent that **does something real with actual operational data** — not just answers questions in a chat. This repo shows the minimum viable pattern: structured input (CSV, but could be a Google Sheet, a database, a Jira export) → deterministic Python logic (what's overdue, for how long) → Claude only for the part that needs natural language (the summary) → output on a real channel (Slack/email).

## Tests

```bash
pytest tests/ -v
```

Covers: CSV parsing (including invalid dates), overdue logic (ignores completed and future tasks), grouping by owner, summary in dry run mode (with and without overdue tasks), Slack/email notification in dry run, and the end-to-end `agent.run()` pipeline.

## License

MIT — use freely in production.

</details>

---

**Feito por [Dimitre Araújo](https://github.com/Dimitrearaujo) — CD Tech**
