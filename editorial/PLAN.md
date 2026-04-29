# Writing improvement plan

> Plano em fases para deixar a doc na qualidade Stripe/Anthropic. Trabalho **só de escrita** — não muda backend, payloads ou comportamento.

**Source of truth**: [`STYLE_GUIDE.md`](./STYLE_GUIDE.md)

---

## Goals

- 0 ocorrências de buzzwords da lista negra
- 100% das aberturas começam com verbo direto
- Headings 100% em sentence case
- Best Practices reduzido a non-obvious (ou removido)
- pt-BR com exemplos localizados (não tradução literal)

---

## Fases

### Fase 0 — Style guide

**Status**: ✅ feito (este arquivo + `STYLE_GUIDE.md`)

**Output**: 9 regras + exemplos antes/depois + checklist de PR.

---

### Fase 1 — Quick wins automatizáveis

**Estimativa**: 2–3h

**Escopo**: tudo que dá pra fazer com regex sem alterar sentido.

| Item | Como | Risco |
|---|---|---|
| Headings → sentence case | sed em lista fixa de headings comuns | baixo |
| "in just X minutes" → cortar | sed | baixo |
| "This endpoint allows you to V X" → "V X" (capitalizado) | script Python com regex | médio |
| "Este endpoint permite V X" → "V X" | mesmo script | médio |
| Substituir buzzwords óbvios (`AI-powered`, `seamlessly`) | grep + revisão manual | baixo |

**Output**: 1 PR "Editorial: sentence case headings + remove filler openers"

**Métrica de sucesso**: rodar
```
grep -rE "This endpoint allows|Este endpoint permite|in just \d+ minute" en/ pt-br/ --include="*.mdx" | wc -l
```
e ver `0`.

---

### Fase 2 — Reescrita das top-10 páginas

**Estimativa**: 1 dia

**Escopo**: as 10 páginas mais lidas. Hipótese inicial:

1. `en/getting-started/quickstart.mdx`
2. `en/getting-started/authentication.mdx`
3. `en/api-reference/endpoints/make-call.mdx`
4. `en/api-reference/endpoints/make-campaign-call.mdx`
5. `en/api-reference/endpoints/create-agent.mdx`
6. `en/api-reference/endpoints/list-calls.mdx`
7. `en/api-reference/endpoints/create-campaign.mdx`
8. `en/api-reference/endpoints/create-webhook.mdx`
9. `en/api-reference/endpoints/update-agent-voice.mdx`
10. `en/introduction.mdx`

> Substituir por dados reais do analytics quando disponível.

**Por página**:
1. Aplicar style guide
2. Cortar "Best Practices" para max 3 bullets non-obvious (ou remover)
3. Substituir tabelas `❌/✅` por prose
4. Trocar exemplos genéricos por contextuais

**Output**: 1 PR "Rewrite top-10 pages" (ou 10 PRs pequenos se preferir).

**Métrica**: revisão manual. Ler em voz alta — se trava, reescreve.

---

### Fase 3 — Editorial pass nas 118 demais

**Estimativa**: 2 dias

**Escopo**: restante das páginas. Pass mais leve — não reescrita do zero.

**Foco**:
- Cortar redundância
- Remover/encurtar Best Practices tautológicas
- Padronizar tom 2ª pessoa
- Aplicar regras 1, 3, 4 do style guide

**Output**: 1 PR "Editorial pass: remaining endpoint pages"

**Métrica**: rodar a `lista negra` do style guide e ver `0`.

---

### Fase 4 — Localização real pt-BR

**Estimativa**: 1 dia

**Escopo**: substituir exemplos genéricos US por contexto BR.

| Tipo | De | Para |
|---|---|---|
| Telefone | `+1234567890`, `+15551234567` | `+5511987654321`, `+5521..` |
| Timezone | `America/New_York` | `America/Sao_Paulo` |
| Nome | "John Doe" | "Maria Silva" |
| Empresa | "Acme Corp" | "Loja Brasil Ltda" |

**Importante**: APIs continuam usando ISO 8601 + E.164. Só os **valores de exemplo** localizam.

**Output**: 1 PR "pt-BR: localize examples"

**Métrica**:
```
grep -rE "\\+1\\d{10}|America/New_York|John Doe" pt-br/ --include="*.mdx" | wc -l
```
deve dar `0` (ou só onde for intencional, ex: agente com clientes US).

---

### Fase 5 — Processo contínuo

**Estimativa**: contínuo

**Escopo**: garantir que doc nova passe pelo style guide.

**Ações**:
1. Adicionar checklist do `STYLE_GUIDE.md` no template `.github/PULL_REQUEST_TEMPLATE.md`
2. Reviewer designado para PRs de doc (rotativo)
3. Quartely audit: rodar a lista negra do style guide, abrir PR de cleanup se ressurgir

---

## Cronograma sugerido

| Semana | Fase | Quem |
|---|---|---|
| 1 | Fase 0 (já feito) + Fase 1 | dev |
| 1–2 | Fase 2 (top-10) | dev + 1 reviewer |
| 3 | Fase 3 (sweep) | dev |
| 4 | Fase 4 (localização) | dev pt-BR speaker |
| 5+ | Fase 5 (processo) | todos |

Total: ~4 semanas focadas, ou 6–8 semanas em paralelo com outro trabalho.

---

## Riscos & mitigação

| Risco | Mitigação |
|---|---|
| Reescrita muda comportamento documentado por acidente | Diff strict por arquivo. Style edit não toca payloads/responses |
| Time discorda do style guide | `STYLE_GUIDE.md` mostra **exemplos do que existe hoje** — fica óbvio o "por quê" |
| pt-BR fica fora de sync com EN após reescrita | EN é fonte de verdade. pt-BR re-traduz quando EN muda. Manter os 2 com mesmo `slug` por arquivo |
| Plano vira backlog eterno | Time-box: Fase 1+2 em 1 sprint. Fase 3 em 1 sprint. Resto em cadence regular |
| Brand whitelabel quebra com reescrita | Manter substituições do `gen_pdf.py apply_brand` testadas — adicionar a esse pipeline o style guide check |

---

## Como medir progresso global

Script único que pode rodar a qualquer momento:

```bash
#!/bin/bash
# editorial/check.sh
cd "$(dirname "$0")/.."

echo "=== Buzzwords ==="
grep -rE "advanced|powerful|comprehensive|seamless|intelligent|cutting-edge|leverage|synergy|robust|AI-powered|AI-driven|world-class|enterprise-grade|sophisticated|in just [0-9]+ minute|This endpoint allows|Este endpoint permite" en/ pt-br/ --include="*.mdx" -l | wc -l | xargs echo "files com buzzword:"

echo "=== Headings Title Case ==="
grep -rE "^## (Request Headers|Request Body|Path Parameters|Query Parameters)" en/ pt-br/ --include="*.mdx" | wc -l | xargs echo "headings em Title Case:"

echo "=== Tabelas ❌/✅ ==="
grep -rE "[✅❌]" en/ pt-br/ --include="*.mdx" -l | wc -l | xargs echo "files com emoji em tabela:"

echo "=== etc. em enum ==="
grep -rE "Options:.*etc\\." en/ pt-br/ --include="*.mdx" | wc -l | xargs echo "etc. em enum:"
```

Meta: todos zerados ao fim da Fase 3.
