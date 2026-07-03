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

**Feito por [Dimitre Araújo](https://github.com/Dimitrearaujo) — CD Tech**
