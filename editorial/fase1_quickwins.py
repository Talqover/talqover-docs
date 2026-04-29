#!/usr/bin/env python3
"""
Fase 1 — quick wins automatizáveis.

Aplica:
  1. Sentence case em headings comuns (lista fixa)
  2. Cortar "in just X minutes" / "em apenas X minutos"
  3. Reescrever openers "This endpoint allows you to V X" -> "Vs X"
  4. Reescrever openers "Este endpoint permite V X" -> "Vs X"
  5. Cortar buzzwords óbvios

Modo seguro: só toca arquivos .mdx em en/ e pt-br/.
Headings só são alterados se a linha começa com #.
"""

from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = [ROOT / "en", ROOT / "pt-br"]

# ---------- 1. Sentence case headings ----------------------------------------
# Mantém siglas e nomes próprios em maiúsculo.
# Substituições case-sensitive de palavra-a-palavra.

HEADING_RENAMES = {
    "Request Headers": "Request headers",
    "Request Body": "Request body",
    "Path Parameters": "Path parameters",
    "Query Parameters": "Query parameters",
    "Error Responses": "Error responses",
    "Error Codes": "Error codes",
    "Best Practices": "Best practices",
    "Important Notes": "Important notes",
    "Example Requests": "Example requests",
    "Response Fields": "Response fields",
    "Validation Rules": "Validation rules",
    "Rate Limits": "Rate limits",
    "Related Endpoints": "Related endpoints",
    "Campaign Calls": "Campaign calls",
    "Individual Agent Calls": "Individual agent calls",
    "When to Use Each Approach": "When to use each approach",
    "Example Use Cases": "Example use cases",
    "Accessing Payload Data": "Accessing payload data",
    "Call Status Flow": "Call status flow",
    "Campaign Payload Usage": "Campaign payload usage",
    "HTTP Headers": "HTTP headers",
    "Survey Flow": "Survey flow",
    "Escalation Rules": "Escalation rules",
    "Custom Responses": "Custom responses",
    "Account-Specific Responses": "Account-specific responses",
    "Contextual Responses": "Contextual responses",
    "Customer Requests": "Customer requests",
    "Advanced Flow": "Advanced flow",
    "Call Flow": "Call flow",
    "Deletion Rules": "Deletion rules",
    "API Endpoints": "API endpoints",
    # pt-BR
    "Cabeçalhos da Requisição": "Cabeçalhos da requisição",
    "Corpo da Requisição": "Corpo da requisição",
    "Parâmetros de Caminho": "Parâmetros de caminho",
    "Parâmetros de Consulta": "Parâmetros de consulta",
    "Respostas de Erro": "Respostas de erro",
    "Códigos de Erro": "Códigos de erro",
    "Boas Práticas": "Boas práticas",
    "Observações Importantes": "Observações importantes",
    "Endpoints Relacionados": "Endpoints relacionados",
    "Campos de Resposta": "Campos de resposta",
    "Regras de Validação": "Regras de validação",
    "Limites de Taxa": "Limites de taxa",
    "Limites de Requisição": "Limites de requisição",
}

# ---------- 2. "in just X minutes" / "em apenas X minutos" -------------------

IN_JUST_PATTERNS = [
    # "...platform in just 5 minutes." -> "...platform."
    (re.compile(r" in just \d+ minutes?\b\.?"), "."),
    (re.compile(r" em apenas \d+ minutos?\b\.?"), "."),
]

# ---------- 3. Openers "This endpoint allows you to V" -----------------------

# EN: imperative -> 3rd person singular present
EN_VERB_MAP = {
    "retrieve": "Retrieves",
    "create": "Creates",
    "update": "Updates",
    "list": "Lists",
    "delete": "Deletes",
    "get": "Gets",
    "modify": "Modifies",
    "configure": "Configures",
    "enable": "Enables",
    "disable": "Disables",
    "toggle": "Toggles",
    "generate": "Generates",
    "verify": "Verifies",
    "query": "Queries",
    "remove": "Removes",
    "add": "Adds",
    "send": "Sends",
    "set": "Sets",
    "make": "Makes",
    "manage": "Manages",
    "manually": None,  # adverb, skip
    "provide": "Provides",
    "activate": "Activates",
    "deactivate": "Deactivates",
}

# PT: infinitivo -> 3a pessoa singular indicativo
PT_VERB_MAP = {
    "criar": "Cria",
    "atualizar": "Atualiza",
    "listar": "Lista",
    "deletar": "Deleta",
    "remover": "Remove",
    "obter": "Obtém",
    "configurar": "Configura",
    "habilitar": "Habilita",
    "desabilitar": "Desabilita",
    "ativar": "Ativa",
    "desativar": "Desativa",
    "verificar": "Verifica",
    "gerar": "Gera",
    "consultar": "Consulta",
    "modificar": "Modifica",
    "enviar": "Envia",
    "alternar": "Alterna",
    "adicionar": "Adiciona",
    "controlar": "Controla",
    "fornecer": "Fornece",
}

EN_OPENER_RE = re.compile(r"\bThis endpoint allows you to (\w+)\b ?", re.IGNORECASE)
PT_OPENER_RE = re.compile(r"\bEste endpoint permite (\w+)\b ?", re.IGNORECASE)
PT_OPENER_QUE_RE = re.compile(r"\bEste endpoint permite que\b ?", re.IGNORECASE)


def rewrite_en_opener(m: re.Match) -> str:
    verb = m.group(1).lower()
    new = EN_VERB_MAP.get(verb)
    if new is None:
        # unknown verb — leave alone (we will warn)
        return m.group(0)
    return f"{new} "


def rewrite_pt_opener(m: re.Match) -> str:
    verb = m.group(1).lower()
    new = PT_VERB_MAP.get(verb)
    if new is None:
        return m.group(0)
    return f"{new} "


# ---------- 4. Buzzwords -----------------------------------------------------

BUZZWORD_REPLACEMENTS = [
    # remove " AI-powered" / " AI-driven" prefix
    (re.compile(r"\bAI-powered (\w)"), lambda m: m.group(1).lower() if False else m.group(1)),
    # simpler: replace as space-eater
    (re.compile(r"\bAI-powered "), ""),
    (re.compile(r"\bAI-driven "), ""),
    (re.compile(r"\bseamlessly "), ""),
    (re.compile(r"\bseamless "), ""),
    (re.compile(r"\bcomprehensive "), ""),
    (re.compile(r"\bpowerful "), ""),
]

# ---------- runner -----------------------------------------------------------

def transform_headings(text: str) -> tuple[str, int]:
    out_lines = []
    n = 0
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("#"):
            for old, new in HEADING_RENAMES.items():
                if old in line:
                    line = line.replace(old, new)
                    n += 1
        out_lines.append(line)
    return "".join(out_lines), n


def transform_in_just(text: str) -> tuple[str, int]:
    n = 0
    for pat, repl in IN_JUST_PATTERNS:
        text, count = pat.subn(repl, text)
        n += count
    return text, n


def transform_openers(text: str, path: Path) -> tuple[str, int]:
    n = 0
    text2, c1 = EN_OPENER_RE.subn(rewrite_en_opener, text)
    text2, c2 = PT_OPENER_RE.subn(rewrite_pt_opener, text2)
    n = c1 + c2
    return text2, n


def transform_buzzwords(text: str) -> tuple[str, int]:
    n = 0
    for pat, repl in BUZZWORD_REPLACEMENTS:
        text, count = pat.subn(repl, text)
        n += count
    return text, n


def main():
    files = []
    for d in TARGETS:
        files.extend(sorted(d.rglob("*.mdx")))

    totals = {"headings": 0, "in_just": 0, "openers": 0, "buzzwords": 0, "files": 0}

    for f in files:
        original = f.read_text()
        text = original
        text, n1 = transform_headings(text)
        text, n2 = transform_in_just(text)
        text, n3 = transform_openers(text, f)
        text, n4 = transform_buzzwords(text)

        if text != original:
            f.write_text(text)
            totals["files"] += 1
        totals["headings"] += n1
        totals["in_just"] += n2
        totals["openers"] += n3
        totals["buzzwords"] += n4

    print(f"files changed: {totals['files']}")
    print(f"  headings sentence-cased: {totals['headings']}")
    print(f"  'in just X minutes' removed: {totals['in_just']}")
    print(f"  openers rewritten: {totals['openers']}")
    print(f"  buzzwords stripped: {totals['buzzwords']}")


if __name__ == "__main__":
    main()
