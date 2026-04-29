# Talkover docs — style guide

> Curto e prático. 9 regras + exemplos extraídos da doc atual. Use no PR review.

---

## 1. Verbo primeiro

Cada endpoint começa com **o verbo direto do que faz**, em 3ª pessoa do indicativo (pt) ou imperativo (en). Sem rodeios.

| ❌ | ✅ |
|---|---|
| "Este endpoint permite criar uma nova ação para o agente." | "Cria uma ação para o agente." |
| "This endpoint allows you to retrieve the agent flow." | "Retorna a configuração de flow do agente." |
| "Use this endpoint to update the campaign status." | "Atualiza o status da campanha." |

**Por quê**: o leitor já sabe que é um endpoint (está numa página de API). A primeira frase precisa carregar **informação**, não cerimônia.

---

## 2. Segunda pessoa

Trate o leitor como `você`. Nunca alterne entre `you`, `we`, `the user`, `the platform`, `our system`.

| ❌ | ✅ |
|---|---|
| "The platform scans the import path..." | "O sistema percorre `import_path`..." (ou: "Você configura `import_path`...") |
| "Our rate limits apply per environment." | "Os limites de taxa se aplicam por ambiente." |
| "We recommend storing the call_id." | "Guarde o `call_id` retornado." |

**Por quê**: voice consistente. Stripe e Anthropic são militantes nisso.

---

## 3. Sentence case nos headings

Apenas a primeira letra maiúscula (e nomes próprios). Nada de `Title Case`.

| ❌ | ✅ |
|---|---|
| `## Request Headers` | `## Request headers` |
| `## Path Parameters` | `## Path parameters` |
| `### Per-status Cooldowns` | `### Per-status cooldowns` |

**Por quê**: parece menos burocrático e mais leve. Padrão atual em docs modernas (Stripe, Anthropic, Linear).

---

## 4. Sem buzzwords vazios

Lista negra (apague na hora):

> `advanced`, `powerful`, `comprehensive`, `seamless`, `intelligent`, `cutting-edge`, `leverage`, `synergy`, `robust`, `AI-powered`, `AI-driven`, `world-class`, `enterprise-grade`, `sophisticated`, `scalable`, `easy`, `easily`, `quickly`

| ❌ | ✅ |
|---|---|
| "Initiate an AI-powered call using a specific voice agent." | "Cria uma chamada com o agente especificado." |
| "advanced automation features" | (liste as features, não chame de "advanced") |
| "comprehensive tracking and reporting" | "tracking" basta |
| "seamless integration" | apenas remova |

**Teste**: se você apagar a palavra e a frase continua **igualmente verdadeira**, ela era ruído. Apague.

---

## 5. Imperativo nos passos

Em getting-started e tutorials, instruções no imperativo.

| ❌ | ✅ |
|---|---|
| "You should send the token in the Authorization header." | "Envie o token no header `Authorization`." |
| "Você deve passar o `agent_id` no path." | "Passe o `agent_id` no path." |

---

## 6. Sem promessas de tempo

Não escreva "in just X minutes", "easily", "quickly". Doc séria não promete experiência.

| ❌ | ✅ |
|---|---|
| "Get started with Talkover in just 5 minutes." | "Quickstart. Após este guia você terá feito sua primeira chamada." |
| "Easily integrate with your CRM." | "Integre com seu CRM via webhook." |

---

## 7. Concreto, não abstrato

Mostre payload real. Não descreva em prose o que um exemplo deixaria óbvio.

| ❌ | ✅ |
|---|---|
| "Custom data to be sent back to your client via webhooks. This data is not used in the conversation but will be included in all webhook events related to this call, allowing you to track and associate calls with your internal records." (71 palavras) | "Metadata anexada à chamada. Devolvida em webhook events. Não afeta a conversa." (12 palavras) + exemplo JSON |

---

## 8. Listas curtas, sem tautologia

`## Best practices` com 5+ bullets genéricos é ruído. Reduza para **2–3 bullets non-obvious** ou remova a seção.

❌ Atual em várias páginas:
```
## Best Practices
1. Always handle errors gracefully
2. Store call IDs
3. Use context for tracking
4. Use is_testing during integration
5. Validate phone numbers
```

✅ Reescrito (apenas o que não é óbvio):
```
## Notes
- Use `Idempotency-Key` em retries para evitar chamadas duplicadas.
- Webhook events só chegam após a chamada terminar — não dependa deles para saber se a call foi aceita.
```

---

## 9. Liste enums, não use "etc."

Se um campo aceita N valores, liste os N. "etc." é doc preguiçosa.

| ❌ | ✅ |
|---|---|
| "Action type. Options: `webhook`, `transfer`, `hold`, etc." | "Action type. Options: `webhook`, `transfer`, `hold`, `external`." |

Se a lista é longa demais (10+), aponte para uma seção dedicada (`/concepts/action-types`).

---

## Exemplos pt-BR localizados

| Tipo | ❌ Genérico | ✅ pt-BR |
|---|---|---|
| Telefone | `+1234567890` | `+5511987654321` |
| Timezone | `America/New_York` | `America/Sao_Paulo` |
| Nome | "John Doe" | "Maria Silva" |
| Empresa | "Acme Corp" | "Loja Brasil Ltda" |
| Moeda em texto | "USD" | "BRL" (quando o exemplo é doméstico) |

**Importante**: API responses ainda usam ISO 8601 (UTC), E.164, números decimais. Não localize os contratos da API — só os valores de exemplo.

---

## Tabelas com emoji ❌/✅

**Só use em comparativos didáticos ou no style guide**, não em doc de endpoint.

❌ Errado: `make-campaign-call.mdx` tem tabela de 7 linhas com emoji ❌/✅ comparando "Campaign Call vs Individual Agent Call". Parece pitch de produto, não doc.

✅ Certo: 1 parágrafo com a regra de decisão.

---

## Naming de IDs em exemplos

Hoje: `agent-uuid-1`, `campaign-uuid-1`, `phone-uuid-1`.

Recomendado (estilo Stripe — mas alinhar com backend antes de mudar):
| Tipo | Prefixo | Exemplo |
|---|---|---|
| Agent | `agt_` | `agt_550e8400e29b41d4a716446655440000` |
| Campaign | `cmp_` | `cmp_d8e2c1...` |
| Call | `call_` | `call_3b2a8...` |
| Webhook | `whk_` | `whk_9fcafb...` |
| Phone | `pn_` | `pn_a1b2c3...` |

**Por quê**: prefixo deixa óbvio o tipo só de olhar. Ajuda no debug. Mas exige mudança no backend — fica como proposta.

---

## Checklist de PR review

Cole isso no template de PR de doc:

```
- [ ] Cada endpoint começa com verbo (sem "this endpoint allows you to" / "este endpoint permite")
- [ ] Headings em sentence case
- [ ] 0 ocorrências de buzzwords da lista negra
- [ ] Tom em 2ª pessoa, consistente
- [ ] "Best practices" ≤3 bullets non-obvious (ou removido)
- [ ] Exemplos pt-BR usam contexto BR (telefone, timezone)
- [ ] Sem "etc." em listagem de enum
- [ ] Sem promessa de tempo ("in just X minutes")
- [ ] Tabelas ❌/✅ apenas se forem mesmo didáticas
```

---

## Lista negra (cole no `grep` antes de mergear)

```bash
grep -rE "advanced|powerful|comprehensive|seamless|intelligent|cutting-edge|leverage|synergy|robust|AI-powered|AI-driven|world-class|enterprise-grade|sophisticated|in just \d+ minute|This endpoint allows|Este endpoint permite" en/ pt-br/ --include="*.mdx"
```

Ideal: zero resultados.
