#!/usr/bin/env python3
"""
Generate a single PDF of the entire Talkover docs (en or pt-br).

Pipeline:
  1. Read docs.json -> ordered list of .mdx pages.
  2. For each .mdx: strip frontmatter, convert MDX components in markdown plain.
  3. (Optional) Apply white-label overrides from clients/<id>.json.
  4. Render to HTML with embedded CSS (palette can be overridden).
  5. Use headless Chrome to print HTML -> PDF.

Output: dist/<brand>-api-docs-<lang>.pdf

Usage:
  python3 tools/gen_pdf.py
  python3 tools/gen_pdf.py --lang pt-br
  python3 tools/gen_pdf.py --client clients/acme.json
  python3 tools/gen_pdf.py --client clients/acme.json --lang pt-br

Client JSON shape (see clients/_template.json):
  {
    "name": "Acme Voice API",
    "tagline": "Voice agents that close",
    "primary_color": "#F97316",
    "accent_color": "#EA580C",
    "domain": "voice.acme.com",
    "api_base_url": "https://voice.acme.com/api/v1",
    "support_email": "support@acme.com",
    "token_prefix": "acme_",
    "websocket_host": "rt.acme.com"
  }
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
DOCS_JSON = ROOT / "docs.json"
DIST = ROOT / "dist"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# ---------- Default branding (Talkover) --------------------------------------

DEFAULT_BRAND = {
    "name": "Talkover API",
    "tagline": "AI-powered voice conversations",
    "primary_color": "#155DFC",
    "accent_color": "#3730a3",
    "domain": "app.talkover.ai",
    "api_base_url": "https://app.talkover.ai/api/v1",
    "support_email": "contact@talkover.ai",
    "support_email_pt": "contato@talkover.ai",
    "token_prefix": "talq_",
    "token_env_name": "TALKOVER_TOKEN",
    "websocket_host": "rt.talkover.ai",
}


def load_brand(client_path: str | None) -> dict:
    if not client_path:
        return DEFAULT_BRAND.copy()
    p = Path(client_path)
    if not p.is_absolute():
        p = ROOT / p
    cfg = json.loads(p.read_text())
    brand = DEFAULT_BRAND.copy()
    brand.update(cfg)
    return brand


# ---------- docs.json -> ordered page list -----------------------------------

def collect_pages(node, out: list[str]) -> None:
    if isinstance(node, str):
        out.append(node)
    elif isinstance(node, dict):
        if "pages" in node:
            for child in node["pages"]:
                collect_pages(child, out)
        if "groups" in node:
            for g in node["groups"]:
                collect_pages(g, out)


def get_pages(lang: str) -> list[tuple[str, str]]:
    cfg = json.loads(DOCS_JSON.read_text())
    langs = cfg["navigation"]["languages"]
    target = next((l for l in langs if l["language"].lower() == lang.lower()), None)
    if not target:
        raise SystemExit(f"language not found in docs.json: {lang}")

    pages: list[tuple[str, str]] = []
    for group in target["groups"]:
        gtitle = group["group"]
        flat: list[str] = []
        collect_pages(group, flat)
        for slug in flat:
            pages.append((gtitle, slug))
    return pages


# ---------- MDX -> markdown plain --------------------------------------------

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
PARAMFIELD_RE = re.compile(r"<ParamField\s+([^>]*?)>(.*?)</ParamField>", re.DOTALL)
PARAMFIELD_SELF_RE = re.compile(r"<ParamField\s+([^/>]*?)/>")
RESPFIELD_RE = re.compile(r"<ResponseField\s+([^>]*?)>(.*?)</ResponseField>", re.DOTALL)
RESPFIELD_SELF_RE = re.compile(r"<ResponseField\s+([^/>]*?)/>")
REQUESTFIELD_RE = re.compile(r"<RequestField\s+([^>]*?)>(.*?)</RequestField>", re.DOTALL)
REQUESTFIELD_SELF_RE = re.compile(r"<RequestField\s+([^/>]*?)/>")
EXAMPLE_BLOCK_RE = re.compile(r"<(RequestExample|ResponseExample)[^>]*>(.*?)</\1>", re.DOTALL)
EXPANDABLE_RE = re.compile(r"<Expandable[^>]*title=\"([^\"]*)\"[^>]*>(.*?)</Expandable>", re.DOTALL)
ADMONITION_RE = re.compile(r"<(Info|Warning|Tip|Note)[^>]*>(.*?)</\1>", re.DOTALL)
ATTR_RE = re.compile(r'(\w+)\s*=\s*(?:"([^"]*)"|\{([^}]*)\})')


def parse_attrs(s: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in ATTR_RE.finditer(s):
        name = m.group(1)
        val = m.group(2) if m.group(2) is not None else m.group(3)
        out[name] = val
    return out


def field_to_md(attrs: str, body: str = "") -> str:
    a = parse_attrs(attrs)
    label = (
        a.get("name") or a.get("path") or a.get("query")
        or a.get("body") or a.get("header") or ""
    )
    typ = a.get("type", "")
    required = "required" in attrs and a.get("required") not in ("false", "{false}")
    default = a.get("default")
    desc = body.strip() if body else ""

    parts = [f"**`{label}`**"]
    if typ:
        parts.append(f"_{typ}_")
    if required:
        parts.append("**required**")
    if default:
        parts.append(f"default: `{default}`")
    line = " · ".join(parts)
    if desc:
        desc_clean = re.sub(r"\n\s*\n", "\n\n  ", desc.strip())
        return f"- {line}\n\n  {desc_clean}\n"
    return f"- {line}\n"


def replace_paramfield(m): return field_to_md(m.group(1), m.group(2))
def replace_paramfield_self(m): return field_to_md(m.group(1), "")


def replace_example(m):
    kind = "Request" if m.group(1) == "RequestExample" else "Response"
    return f"\n**{kind} example**\n\n{m.group(2).strip()}\n"


def replace_expandable(m):
    return f"\n**{m.group(1)}**\n\n{m.group(2).strip()}\n"


def replace_admonition(m):
    return f"\n> **{m.group(1)}.** {m.group(2).strip()}\n"


def mdx_to_md(text: str) -> str:
    fm = FRONTMATTER_RE.match(text)
    if fm:
        text = text[fm.end():]
    text = ADMONITION_RE.sub(replace_admonition, text)
    text = EXPANDABLE_RE.sub(replace_expandable, text)
    text = EXAMPLE_BLOCK_RE.sub(replace_example, text)
    text = PARAMFIELD_RE.sub(replace_paramfield, text)
    text = PARAMFIELD_SELF_RE.sub(replace_paramfield_self, text)
    text = RESPFIELD_RE.sub(replace_paramfield, text)
    text = RESPFIELD_SELF_RE.sub(replace_paramfield_self, text)
    text = REQUESTFIELD_RE.sub(replace_paramfield, text)
    text = REQUESTFIELD_SELF_RE.sub(replace_paramfield_self, text)
    text = re.sub(r"</?[A-Z][A-Za-z0-9]*[^>]*>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


# ---------- White-label rebrand ----------------------------------------------

def apply_brand(text: str, brand: dict) -> str:
    """
    Substitute every Talkover-specific reference with client-specific values.
    Order matters: most specific patterns first.
    """
    # API base URL
    text = text.replace("https://app.talkover.ai/api/v1", brand["api_base_url"])
    text = text.replace(
        "app.talkover.ai/api/v1",
        brand["api_base_url"].replace("https://", "").replace("http://", ""),
    )
    # Bare domain
    if brand["domain"] != DEFAULT_BRAND["domain"]:
        text = text.replace("app.talkover.ai", brand["domain"])
    # Emails (en + pt)
    if brand["support_email"] != DEFAULT_BRAND["support_email"]:
        text = text.replace("contact@talkover.ai", brand["support_email"])
        text = text.replace("contact@talkover.com", brand["support_email"])
    pt_email = brand.get("support_email_pt") or brand["support_email"]
    if pt_email != DEFAULT_BRAND["support_email_pt"]:
        text = text.replace("contato@talkover.ai", pt_email)
        text = text.replace("contato@talkover.com", pt_email)
    # Token prefix (talq_xxx -> client_xxx)
    if brand["token_prefix"] != DEFAULT_BRAND["token_prefix"]:
        text = re.sub(r"\btalq_", brand["token_prefix"], text)
    # ENV variable name (TALKOVER_TOKEN -> CLIENT_TOKEN)
    if brand["token_env_name"] != DEFAULT_BRAND["token_env_name"]:
        text = text.replace("TALKOVER_TOKEN", brand["token_env_name"])
    # WebSocket host
    if brand["websocket_host"] != DEFAULT_BRAND["websocket_host"]:
        text = text.replace("rt.talkover.ai", brand["websocket_host"])
    # Bare residual reference to talkover domain (without app.)
    if brand["domain"] != DEFAULT_BRAND["domain"] and "talkover" not in brand["domain"]:
        text = re.sub(r"\btalkover\.ai\b", brand["domain"], text)
    # Brand name — most specific first
    if brand["name"] != DEFAULT_BRAND["name"]:
        bare_name = brand.get("company_name") or (
            brand["name"].replace(" API", "").replace(" Voice API", "")
        )
        text = text.replace("Talkover API", brand["name"])
        text = text.replace("Talkover", bare_name)
        text = text.replace("talkover", bare_name.lower())
    return text


# ---------- Build HTML --------------------------------------------------------

CSS_TEMPLATE = """
@page { size: A4; margin: 18mm 16mm 20mm 16mm; }
body { font-family: -apple-system, "Segoe UI", system-ui, sans-serif; font-size: 10.5pt; line-height: 1.55; color: #1f2937; }
h1, h2, h3, h4 { color: #0f172a; }
h1 { font-size: 22pt; border-bottom: 2px solid {{primary}}; padding-bottom: 4pt; margin-top: 28pt; page-break-before: always; }
h1:first-of-type { page-break-before: avoid; }
h2 { font-size: 15pt; margin-top: 18pt; border-bottom: 1px solid #e5e7eb; padding-bottom: 2pt; }
h3 { font-size: 12.5pt; margin-top: 12pt; color: {{primary}}; }
h4 { font-size: 11pt; margin-top: 10pt; }
code, pre { font-family: "SF Mono", Menlo, Consolas, monospace; }
pre { background: #0f172a; color: #e2e8f0; padding: 8pt 10pt; border-radius: 4pt; font-size: 8.5pt; line-height: 1.35; white-space: pre-wrap; word-break: break-word; page-break-inside: avoid; }
:not(pre) > code { background: #eef2ff; color: {{accent}}; padding: 1pt 4pt; border-radius: 3pt; font-size: 9pt; }
blockquote { border-left: 3px solid #f59e0b; background: #fffbeb; padding: 6pt 10pt; margin: 10pt 0; page-break-inside: avoid; }
table { width: 100%; border-collapse: collapse; margin: 8pt 0; font-size: 9.5pt; }
th, td { border: 1px solid #e5e7eb; padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { background: #f8fafc; }
ul, ol { padding-left: 18pt; }
li { margin: 2pt 0; }
hr { border: none; border-top: 1px solid #cbd5e1; margin: 16pt 0; }
.cover { text-align: center; padding-top: 80pt; page-break-after: always; }
.cover h1 { border: none; font-size: 36pt; margin-bottom: 8pt; page-break-before: avoid; color: {{primary}}; }
.cover .tagline { color: #475569; font-size: 14pt; margin-top: 0; }
.cover .meta { color: #94a3b8; font-size: 10pt; margin-top: 40pt; }
.toc { page-break-after: always; }
.toc a { color: {{primary}}; text-decoration: none; }
.toc ol { padding-left: 22pt; }
.endpoint-meta { color: #64748b; font-size: 9pt; margin: 0 0 6pt 0; }
"""


def build_css(brand: dict) -> str:
    return (
        CSS_TEMPLATE
        .replace("{{primary}}", brand["primary_color"])
        .replace("{{accent}}", brand["accent_color"])
    )


def build_html(lang: str, pages: list[tuple[str, str]], brand: dict) -> str:
    parts: list[str] = []
    parts.append("<!doctype html><html><head><meta charset='utf-8'>")
    parts.append(f"<title>{brand['name']} ({lang})</title>")
    parts.append(f"<style>{build_css(brand)}</style></head><body>")

    parts.append(
        "<div class='cover'>"
        f"<h1>{brand['name']}</h1>"
        f"<p class='tagline'>{brand['tagline']}</p>"
        f"<p class='meta'>Full API reference · {lang}<br/>{brand['api_base_url']}</p>"
        "</div>"
    )

    parts.append("<div class='toc'><h1>Contents</h1><ol>")
    last_group = None
    for gtitle, slug in pages:
        slug_id = slug.replace("/", "-")
        if gtitle != last_group:
            if last_group is not None:
                parts.append("</ol></li>")
            parts.append(f"<li><strong>{gtitle}</strong><ol>")
            last_group = gtitle
        parts.append(f"<li><a href='#{slug_id}'>{slug.split('/')[-1]}</a></li>")
    if last_group is not None:
        parts.append("</ol></li>")
    parts.append("</ol></div>")

    last_group = None
    md_converter = markdown.Markdown(extensions=["fenced_code", "tables", "sane_lists"])

    for gtitle, slug in pages:
        slug_id = slug.replace("/", "-")
        path = ROOT / f"{slug}.mdx"
        if not path.exists():
            print(f"  ! missing: {path}", file=sys.stderr)
            continue
        raw = path.read_text()
        md = mdx_to_md(raw)
        md = apply_brand(md, brand)

        if gtitle != last_group:
            parts.append(f"<h1 class='group-title'>{gtitle}</h1>")
            last_group = gtitle

        parts.append(f"<a id='{slug_id}'></a>")
        html_body = md_converter.reset().convert(md)
        parts.append(f"<div class='endpoint-meta'>{slug}.mdx</div>")
        parts.append(html_body)
        parts.append("<hr/>")

    parts.append("</body></html>")
    return "\n".join(parts)


# ---------- Chrome headless -> PDF -------------------------------------------

def html_to_pdf(html_path: Path, pdf_path: Path) -> None:
    if not Path(CHROME).exists():
        raise SystemExit(f"chrome not found at {CHROME}")
    cmd = [
        CHROME, "--headless", "--disable-gpu", "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        f"file://{html_path}",
    ]
    print("running:", " ".join(cmd[:4]), "...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.stderr.write(res.stderr)
        raise SystemExit("chrome failed")


# ---------- Main --------------------------------------------------------------

def slugify_brand(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "client"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="en", help="en or pt-br (default: en)")
    ap.add_argument("--client", default=None, help="path to clients/<id>.json for white-label")
    args = ap.parse_args()

    brand = load_brand(args.client)
    brand_slug = brand.get("slug") or slugify_brand(brand["name"])

    DIST.mkdir(exist_ok=True)
    pages = get_pages(args.lang)
    print(f"brand: {brand['name']} ({brand['domain']})")
    print(f"collected {len(pages)} pages for {args.lang}")

    html = build_html(args.lang, pages, brand)
    html_path = DIST / f"{brand_slug}-docs-{args.lang}.html"
    pdf_path = DIST / f"{brand_slug}-docs-{args.lang}.pdf"
    html_path.write_text(html)
    print(f"html: {html_path} ({html_path.stat().st_size // 1024} KB)")

    html_to_pdf(html_path, pdf_path)
    print(f"pdf:  {pdf_path} ({pdf_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
