# PR Description

<!-- O que esta PR muda? Em 1–3 frases. -->

## Type of change

<!-- Marque uma -->

- [ ] Conteúdo novo (novo endpoint, nova guide, nova página)
- [ ] Atualização de doc existente (mudança de payload, fix técnico)
- [ ] Editorial (estilo, redação, gramática)
- [ ] Tooling (scripts, build, CI)

## Editorial checklist

> Aplicável a qualquer PR que toque `.mdx` em `en/` ou `pt-br/`. Veja `editorial/STYLE_GUIDE.md` para detalhes.

- [ ] Cada endpoint começa com **verbo direto** (sem "this endpoint allows you to" / "este endpoint permite")
- [ ] Headings em **sentence case** (`## Request body`, não `## Request Body`)
- [ ] **Tom em 2ª pessoa**, consistente (sem mistura "you" / "we" / "the platform")
- [ ] Sem **buzzwords** da lista negra (`advanced`, `powerful`, `comprehensive`, `seamless`, `intelligent`, `cutting-edge`, `leverage`, `synergy`, `robust`, `AI-powered`, `AI-driven`, `world-class`, `enterprise-grade`, `sophisticated`)
- [ ] **"Best practices" ≤ 3 bullets non-obvious** ou removido (não em páginas de endpoint)
- [ ] **Sem `etc.`** em listas de enum — listar todos os valores
- [ ] **Sem promessa de tempo** ("in just X minutes")
- [ ] Tabelas **sem emoji** ❌/✅
- [ ] Exemplos **pt-BR usam contexto BR** (telefone `+5511...`, timezone `America/Sao_Paulo`, nomes BR)

## Verificação automática

Antes de mergear, rode:

```bash
bash editorial/check.sh
```

Todos os contadores devem estar em **0** (exceto seções legítimas em guides/concepts).

## API change?

Se esta PR muda payload, response shape, status code ou comportamento de endpoint:

- [ ] Backend correspondente já está em produção / atrás de feature flag
- [ ] `openapi.json` (em `api-reference/`) atualizado
- [ ] Versão / changelog atualizado (quando existir)

## pt-BR

- [ ] Conteúdo equivalente em `pt-br/` foi atualizado
- [ ] Exemplos em pt-BR estão localizados (não tradução literal de texto US)

## PDFs (se for release de marca)

- [ ] `python3 tools/gen_pdf.py` rodou sem erro (Talkover default)
- [ ] PDFs whitelabel (`--client clients/<id>.json`) regenerados se config de cliente mudou
