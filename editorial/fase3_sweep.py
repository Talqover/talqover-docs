#!/usr/bin/env python3
"""
Fase 3 — editorial sweep nas 118 demais páginas.

Aplica:
  1. Remove section "## Best practices" / "## Boas práticas" em
     api-reference/endpoints/*.mdx (mantém em guides/).
     Razão: são tautológicas em quase todas as páginas. Doc de referência
     não é lugar pra "Always handle errors gracefully".
  2. Simplifica "You can find this in your dashboard under X" — remove a
     frase, mantém o resto.
  3. "Detailed description of what the action does" -> "What the action does"
  4. Substitui "Acme Corp" por "Loja Brasil" em exemplos pt-BR; mantém em EN
     mas neutraliza pra "Demo with Acme" (sem Corp/Inc — fica genérico).
"""

from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN = ROOT / "en"
PTBR = ROOT / "pt-br"


def remove_best_practices(text: str) -> tuple[str, int]:
    """Remove ## Best practices ... até próxima seção ## ou EOF."""
    # EN
    pat_en = re.compile(r"\n## Best practices\n.*?(?=\n## |\Z)", re.DOTALL)
    # PT
    pat_pt = re.compile(r"\n## Boas práticas\n.*?(?=\n## |\Z)", re.DOTALL)
    n = 0
    text, c1 = pat_en.subn("\n", text)
    text, c2 = pat_pt.subn("\n", text)
    return text, c1 + c2


def simplify_dashboard_phrase(text: str) -> tuple[str, int]:
    patterns = [
        # EN: " You can find this in your dashboard under X." → ""
        (re.compile(r"\.?\s*You can find this in your dashboard under [A-Za-z ]+\."), "."),
        (re.compile(r"\.?\s*Você pode encontrá-lo em seu painel,? na seção [A-Za-z ]+\."), "."),
        (re.compile(r"\.?\s*Você pode encontrá-lo no seu painel,? na seção [A-Za-z ]+\."), "."),
        (re.compile(r"\.?\s*Você pode encontrar isto em seu painel,? na seção [A-Za-z ]+\."), "."),
    ]
    n = 0
    for pat, repl in patterns:
        text, c = pat.subn(repl, text)
        n += c
    # cleanup: ".." → "."
    text = re.sub(r"\.\.+", ".", text)
    return text, n


def trim_descriptions(text: str) -> tuple[str, int]:
    pairs = [
        ("Detailed description of what the action does", "What the action does"),
        ("Detailed description of the action", "What the action does"),
        ("Descrição detalhada do que a ação faz", "O que a ação faz"),
    ]
    n = 0
    for a, b in pairs:
        if a in text:
            text = text.replace(a, b)
            n += 1
    return text, n


def neutralize_acme(text: str, is_pt: bool) -> tuple[str, int]:
    n = 0
    # "Acme Corp" / "Acme Inc" -> drop suffix (apenas Acme) ou trocar
    if is_pt:
        # pt-br: Acme Corp -> Loja Brasil
        if "Acme Corp" in text:
            text = text.replace("Acme Corp", "Loja Brasil")
            n += 1
        if "Acme Inc" in text:
            text = text.replace("Acme Inc", "Loja Brasil")
            n += 1
    else:
        # en: Acme Corp -> Acme (mais neutro)
        if "Acme Corp" in text:
            text = text.replace("Acme Corp", "Acme")
            n += 1
        if "Acme Inc" in text:
            text = text.replace("Acme Inc", "Acme")
            n += 1
    return text, n


def process(path: Path, is_pt: bool, only_endpoints: bool) -> dict:
    original = path.read_text()
    text = original
    counts = {"bp": 0, "dash": 0, "trim": 0, "acme": 0}

    if only_endpoints:
        text, counts["bp"] = remove_best_practices(text)
    text, counts["dash"] = simplify_dashboard_phrase(text)
    text, counts["trim"] = trim_descriptions(text)
    text, counts["acme"] = neutralize_acme(text, is_pt)

    if text != original:
        path.write_text(text)
    return counts


def main():
    totals = {"bp": 0, "dash": 0, "trim": 0, "acme": 0, "files": 0}

    for root, locale in [(EN, "en"), (PTBR, "pt-br")]:
        is_pt = locale == "pt-br"
        # 1. Endpoints — remove best practices + outros
        for f in (root / "api-reference" / "endpoints").rglob("*.mdx"):
            counts = process(f, is_pt, only_endpoints=True)
            for k in totals:
                if k != "files":
                    totals[k] += counts.get(k, 0)
            if any(counts.values()):
                totals["files"] += 1
        # 2. Resto (guides, concepts, getting-started) — sem remover best practices
        for sub in ["guides", "concepts", "getting-started"]:
            d = root / sub
            if not d.exists():
                continue
            for f in d.rglob("*.mdx"):
                counts = process(f, is_pt, only_endpoints=False)
                for k in totals:
                    if k != "files":
                        totals[k] += counts.get(k, 0)
                if any(counts.values()):
                    totals["files"] += 1
        # 3. Top-level files
        for f in root.glob("*.mdx"):
            counts = process(f, is_pt, only_endpoints=False)
            for k in totals:
                if k != "files":
                    totals[k] += counts.get(k, 0)
            if any(counts.values()):
                totals["files"] += 1

    print(f"files changed: {totals['files']}")
    print(f"  Best practices sections removed: {totals['bp']}")
    print(f"  'You can find this in dashboard' simplified: {totals['dash']}")
    print(f"  Verbose descriptions trimmed: {totals['trim']}")
    print(f"  Acme Corp/Inc neutralized: {totals['acme']}")


if __name__ == "__main__":
    main()
