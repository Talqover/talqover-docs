# Talkover API — Routes Audit

> **Como usar**: marque `[x]` nas rotas que quer expor na doc pública. Deixe `[ ]` nas que NÃO devem ir pra doc.
>
> Legenda de status (vs doc atual em `talkover-docs/`):
> - 🆕 **NOVA** — não existe na doc atual
> - ✏️ **MUDOU** — existe na doc mas payload/response divergiu
> - ✅ **JÁ DOC** — existe e está atualizada
> - ⚠️ **REMOVER** — está na doc atual mas não existe mais no backend / não deve ser exposta
>
> Buckets:
> - 🟢 **PÚBLICO** — `EnvironmentTokenAuth` (token de customer)
> - 🔵 **SESSÃO** — `auth:sanctum` (dashboard / token de usuário humano)
> - 🟡 **WEBHOOK INBOUND** — chamado por provedor externo
> - 🔴 **INFRA/INTERNO** — worker, telephony, admin, monitoring
>
> Nomes de provedores (Twilio/Telnyx/TalkPhone/Pipecat/Daily/Stripe/Documenso/ElevenLabs/Google/Typeform) **não devem aparecer** na doc — somos SaaS.

---

## 🟢 Public API — `EnvironmentTokenAuth`

### Agents — CRUD

- [ ] ✅ `GET /v1/agents` — list agents (query: `status`, `direction`, `search`, `per_page`)
- [ ] ✏️ `POST /v1/agents` — create agent **(payload mudou: novos required `endpointing_sensitivity`, `ivr_navigation_mode`, `conversation_speed`, `initial_message_delay`, `idle_time_seconds`, `llm_temperature`, `enable_recording`, `who_speaks_first`; novos opcionais `max_idle_check_count`, `max_call_duration_seconds`, `say_goodbye_on_max_duration`, `user_inactivity_timeout_seconds`, `initial_idle_time_seconds`, `initial_max_idle_check_count`, `phone_number_ids[]`)**
- [ ] ✅ `GET /v1/agents/{agent}` — get agent
- [ ] ✅ `DELETE /v1/agents/{agent}` — delete agent
- [ ] ✅ `PUT /v1/agents/{agent}/knowledge` — update knowledge fields
- [ ] ✏️ `PUT /v1/agents/{agent}/voice` — update voice **(`similarity` e `stability` agora condicionais a high-fidelity voices; range de `conversation_speed` divergente do create)**
- [ ] 🆕 `PUT /v1/agents/{agent}/calling` — update calling config (direction + phone_number_ids[])
- [ ] 🆕 `POST /v1/agents/{agent}/publish` — publish agent
- [ ] 🆕 `POST /v1/agents/{agent}/unpublish` — unpublish agent

### Agents — Templates 🆕

- [x] 🆕 `GET /v1/agents/templates` — list templates (query: `country_code`)
- [x] 🆕 `GET /v1/agents/templates/sectors` — templates by sector (query: `builder_type=general|flow`)
- [x] 🆕 `GET /v1/agents/templates/search` — search templates (query: `query` min:2)
- [x] 🆕 `GET /v1/agents/templates/statistics` — template statistics ⚠️ revisar se é admin-only
- [x] 🆕 `POST /v1/agents/templates/create` — create agent from template
- [x] 🆕 `POST /v1/agents/templates/clone` — clone template into existing agent ⚠️ controller tem `dd()` (bug — confirmar com backend)

### Agents — Advanced 🆕

- [ ] 🆕 `GET /v1/agents/{agent}/optimized-costs-eligibility` — eligibility check (≥700 calls/7d)
- [ ] 🆕 `PATCH /v1/agents/{agent}/advanced-settings` — toggle initial message cache, etc.

### Agents — Pricing 🆕

- [ ] 🆕 `GET /v1/agents/{agent}/pricing` — pricing breakdown
- [ ] 🆕 `GET /v1/agents/{agent}/pricing/summary` — pricing summary

### Agent Trainings

- [ ] ✅ `GET /v1/agents/{agent}/trainings` — list trainings
- [ ] ✅ `POST /v1/agents/{agent}/trainings` — upsert training (by `node_id`)
- [ ] ✅ `DELETE /v1/agents/{agent}/trainings/{training}` — delete training

### Agent Actions

- [ ] ✅ `GET /v1/agents/{agent}/actions` — list actions
- [ ] ✏️ `POST /v1/agents/{agent}/actions` — upsert action **(novos: `authorization_scheme`, `custom_headers[]`, `speak_on_send`, `speak_on_receive`, `execution_mode`, `integration:{id}`)**
- [ ] ✅ `DELETE /v1/agents/{agent}/actions/{action}` — delete action

### Agent Webhooks

- [ ] ✅ `GET /v1/agents/{agent}/webhooks` — list webhooks + available events
- [ ] ✏️ `POST /v1/agents/{agent}/webhooks` — create webhook **(novos: `authorization_scheme`, `custom_headers[]`, `http_method`, `payload_templates`)**
- [ ] ✅ `GET /v1/agents/{agent}/webhooks/{webhook}` — get webhook
- [ ] ✏️ `PUT /v1/agents/{agent}/webhooks/{webhook}` — update webhook (mesmos novos campos)
- [ ] ✅ `DELETE /v1/agents/{agent}/webhooks/{webhook}` — delete webhook
- [ ] ✅ `PATCH /v1/agents/{agent}/webhooks/{webhook}/toggle` — enable/disable
- [ ] ✅ `POST /v1/agents/{agent}/webhooks/{webhook}/test` — send test payload
- [ ] 🆕 `GET /v1/agents/{agent}/webhooks/{webhook}/logs` — list delivery logs
- [ ] 🆕 `POST /v1/agents/{agent}/webhooks/{webhook}/logs/{log}/retry` — retry failed delivery

### Agent Flow (Conversation Flow) 🆕

> ⚠️ Não citar "Pipecat" na doc — chamar de "Conversation Flow" ou "Agent Flow".

- [ ] 🆕 `GET /v1/agents/{agent}/flow` — get current flow + mode
- [ ] 🆕 `PUT /v1/agents/{agent}/flow` — update flow (`conversation_mode`, `flow_config`)
- [ ] 🆕 `POST /v1/agents/{agent}/flow/validate` — validate flow config
- [ ] 🆕 `GET /v1/agents/{agent}/flow/versions` — list flow versions

### Callback Agents 🆕

- [ ] 🆕 `GET /v1/callback-agents` — list callback agents
- [ ] 🆕 `GET /v1/callback-agents/source-agents` — eligible outbound agents
- [ ] 🆕 `GET /v1/callback-agents/stats` — callback stats (date range)
- [ ] 🆕 `GET /v1/callback-agents/{agent}` — get callback agent + sources + stats
- [ ] 🆕 `POST /v1/callback-agents/{agent}/check-constraints` — validate config
- [ ] 🆕 `POST /v1/agents/{agent}/callback` — set agent as callback
- [ ] 🆕 `PUT /v1/agents/{agent}/callback` — update callback sources
- [ ] 🆕 `DELETE /v1/agents/{agent}/callback` — remove callback role

### Calls

- [ ] ✅ `GET /v1/calls` — list calls (filtros amplos)
- [ ] ✅ `GET /v1/agents/{agent}/calls` — list calls of agent
- [ ] ✏️ `POST /v1/agents/{agent}/call` — make call **(novos: `context`, `delay_seconds (0–3600)`, `is_testing`; ⚠️ branch interno expõe websocket worker — NÃO documentar branch externo)**
- [ ] ✏️ `POST /v1/campaigns/{campaign}/call` — make campaign call **(novos: `context`, `allow_duplicates`, `is_testing`; retorna 409 com `existing_call`)**
- [ ] 🆕 `POST /v1/agents/{agent}/end-call` — hangup active call
- [ ] 🆕 `GET /v1/agents/{agent}/active-call/{phone}` — find active call by phone
- [ ] ⚠️ `make-external-call` — **rota separada não existe mais; rota foi absorvida em `makeCall`. Remover a página `make-external-call.mdx`.**

### Call Summaries (Analytics) 🆕

- [x] 🆕 `GET /v1/call-summaries` — dashboard data (granularity hourly/daily/weekly/monthly, max range varia)
- [x] 🆕 `GET /v1/call-summaries/totals` — totals (max 365d)
- [x] 🆕 `DELETE /v1/call-summaries/cache` — clear cache (avaliar se merece estar na doc pública)

### Campaigns

- [ ] ✅ `GET /v1/campaigns` — list campaigns
- [ ] ✏️ `POST /v1/campaigns` — create campaign **(payload mudou bastante: `call_time_ranges[{start,end}]` no lugar de earliest/latest, cooldowns por status, DNC com source environment/global/custom + `do_not_call_custom_list[]`, `auto_add_to_dnc_*`, `retry_on_no_conversion`, `enable_post_completion_cooldown`)**
- [ ] ✅ `GET /v1/campaigns/{campaign}` — get campaign
- [ ] ✏️ `PUT /v1/campaigns/{campaign}` — update campaign (mesmos novos campos)
- [ ] ✅ `DELETE /v1/campaigns/{campaign}` — delete campaign (bloqueia se tem calls ativas)
- [ ] ✅ `PATCH /v1/campaigns/{campaign}/status` — update status

### Campaign Webhooks 🆕

> Mesma estrutura dos Agent Webhooks + campo extra `include_call_events`. Eventos: `campaign_call.{queued|started|completed|retry_scheduled|failed}`, `campaign.{created|started|paused|completed|updated}`, `event_recording`, `event_call_transcript`, `event_call_report`.

- [ ] 🆕 `GET /v1/campaigns/{campaign}/webhooks` — list
- [ ] 🆕 `POST /v1/campaigns/{campaign}/webhooks` — create
- [ ] 🆕 `GET /v1/campaigns/{campaign}/webhooks/{webhook}` — show
- [ ] 🆕 `PUT /v1/campaigns/{campaign}/webhooks/{webhook}` — update
- [ ] 🆕 `DELETE /v1/campaigns/{campaign}/webhooks/{webhook}` — delete
- [ ] 🆕 `PATCH /v1/campaigns/{campaign}/webhooks/{webhook}/toggle` — toggle
- [ ] 🆕 `POST /v1/campaigns/{campaign}/webhooks/{webhook}/test` — test
- [ ] 🆕 `GET /v1/campaigns/{campaign}/webhooks/{webhook}/logs` — logs
- [ ] 🆕 `POST /v1/campaigns/{campaign}/webhooks/{webhook}/logs/{log}/retry` — retry

### Campaign SFTP 🆕

- [ ] 🆕 `GET /v1/campaigns/{campaign}/sftp` — show config
- [ ] 🆕 `POST /v1/campaigns/{campaign}/sftp` — create config (sempre disabled inicial)
- [ ] 🆕 `PUT /v1/campaigns/{campaign}/sftp` — update (requer test antes de habilitar)
- [ ] 🆕 `POST /v1/campaigns/{campaign}/sftp/test-connection` — test connection
- [ ] 🆕 `POST /v1/campaigns/{campaign}/sftp/trigger-import` — trigger import job
- [ ] 🆕 `POST /v1/campaigns/{campaign}/sftp/trigger-export` — trigger export (`file_data_ids[]`)
- [ ] 🆕 `GET /v1/campaigns/{campaign}/sftp/logs` — logs

### Phone Numbers

- [ ] ✅ `GET /v1/phone-numbers` — list (filtros: `direction`, `type`, `has_voice`, `search`)
- [ ] 🆕 `GET /v1/phone-numbers/release-requests` — list release requests
- [ ] 🆕 `POST /v1/phone-numbers/{phoneNumber}/request-release` — request release (`reason` 10–500)
- [ ] 🆕 `DELETE /v1/phone-numbers/release-requests/{releaseRequest}` — cancel request

### Voice Templates

- [ ] ✅ `GET /v1/voice-templates` — list (filtros: `language`, `quality_tier`, `gender`)
- [ ] ✅ `GET /v1/voice-templates/{voiceTemplate}/demo` — signed mp3 URL

### Action Integrations 🆕

- [ ] 🆕 `GET /v1/action-integrations` — catálogo de integrações
- [x] 🆕 `GET /v1/action-integrations/category/{category}` — por categoria
- [x] 🆕 `GET /v1/action-integrations/{identifier}/config` — schema de config

### Calendars (Calendar Core) 🆕

> ⚠️ Provedores externos (Google) NÃO devem aparecer na doc — chamar "Calendar Provider Integration".

- [ ] 🆕 `GET /v1/calendars` — list
- [ ] 🆕 `POST /v1/calendars` — create
- [ ] 🆕 `GET /v1/calendars/events` — batch events (calendar_ids[]+from+to)
- [ ] 🆕 `POST /v1/calendars/sync` — trigger sync
- [ ] 🆕 `GET /v1/calendars/sync-status` — sync status
- [ ] 🆕 `GET /v1/calendars/{calendar}` — show
- [ ] 🆕 `PUT /v1/calendars/{calendar}` — update
- [ ] 🆕 `DELETE /v1/calendars/{calendar}` — delete

#### Calendar Members
- [ ] 🆕 `GET /v1/calendars/{calendar}/members` — list members
- [ ] 🆕 `POST /v1/calendars/{calendar}/members` — add member
- [ ] 🆕 `PUT /v1/calendars/{calendar}/members/{member}` — update member
- [ ] 🆕 `DELETE /v1/calendars/{calendar}/members/{member}` — remove member

#### Calendar Events
- [ ] 🆕 `GET /v1/calendars/{calendar}/events` — list events
- [ ] 🆕 `POST /v1/calendars/{calendar}/events` — create event
- [ ] 🆕 `GET /v1/calendars/{calendar}/events/{event}` — show event
- [ ] 🆕 `PUT /v1/calendars/{calendar}/events/{event}` — update event
- [ ] 🆕 `DELETE /v1/calendars/{calendar}/events/{event}` — delete event
- [ ] 🆕 `POST /v1/calendars/{calendar}/events/{event}/meeting` — create meeting link

#### Calendar Event Attendees
- [ ] 🆕 `POST /v1/calendars/{calendar}/events/{event}/attendees` — add attendee
- [ ] 🆕 `DELETE /v1/calendars/{calendar}/events/{event}/attendees/{attendee}` — remove attendee

#### Calendar Availability
- [ ] 🆕 `GET /v1/calendars/{calendar}/availability-rules` — list rules
- [ ] 🆕 `POST /v1/calendars/{calendar}/availability-rules` — create rule
- [ ] 🆕 `PUT /v1/calendars/{calendar}/availability-rules/{rule}` — update rule
- [ ] 🆕 `DELETE /v1/calendars/{calendar}/availability-rules/{rule}` — delete rule
- [ ] 🆕 `GET /v1/calendars/{calendar}/availability` — query availability

#### Calendar Provider Connections
- [ ] 🆕 `GET /v1/calendars/{calendar}/providers` — list connections
- [ ] 🆕 `POST /v1/calendars/{calendar}/providers` — create connection (OAuth-style)
- [ ] 🆕 `DELETE /v1/calendars/{calendar}/providers/{provider}` — disconnect
- [ ] 🆕 `POST /v1/calendars/{calendar}/providers/{provider}/sync` — trigger provider sync

### Auto Topup 🆕

> ⚠️ Esconder nomes de payment provider — expor só `card.brand/last4/exp_*`.

- [ ] 🆕 `GET /v1/auto-topup/settings` — get settings
- [ ] 🆕 `PUT /v1/auto-topup/settings` — update settings
- [ ] 🆕 `POST /v1/auto-topup/test` — trigger test recharge
- [ ] 🆕 `POST /v1/auto-topup/disable` — disable
- [ ] 🆕 `GET /v1/auto-topup/history` — recharge history
- [ ] 🆕 `GET /v1/auto-topup/payment-methods` — list payment methods

### Subscription Features 🆕

- [x] 🆕 `GET /v1/subscription-features/usage-summary` — usage vs limits
- [x] 🆕 `GET /v1/subscription-features/can-create-agent` — check
- [x] 🆕 `GET /v1/subscription-features/can-create-campaign` — check
- [x] 🆕 `GET /v1/subscription-features/can-make-concurrent-call` — check
- [x] 🆕 `GET /v1/subscription-features/next-plan` — upgrade target

### SIP Trunks (Custom) 🆕

> Atrás de feature flag `allow_custom_sip_trunks` (Enterprise).

- [ ] 🆕 `GET /v1/sip-trunks` — list
- [ ] 🆕 `POST /v1/sip-trunks` — create (`name`, `provider_name`, `domain`, `username`, `password`, `port`, `transport (udp|tcp|tls)`, `outbound_proxy`, `auth_realm`, `is_active`)
- [ ] 🆕 `GET /v1/sip-trunks/{trunkId}` — show
- [ ] 🆕 `PUT /v1/sip-trunks/{trunkId}` — update
- [ ] 🆕 `DELETE /v1/sip-trunks/{trunkId}` — delete
- [ ] 🆕 `POST /v1/sip-trunks/{trunkId}/verify` — verify trunk
- [ ] 🆕 `GET /v1/sip-trunks/{trunkId}/health` — health check
- [ ] 🆕 `GET /v1/sip-trunks/{trunkId}/dids` — list DIDs
- [ ] 🆕 `POST /v1/sip-trunks/{trunkId}/dids` — create DID (`country_code`, `number`)
- [ ] 🆕 `DELETE /v1/sip-trunks/{trunkId}/dids/{phoneNumberId}` — delete DID

### External Form Trigger 🆕

> ⚠️ Não citar "Typeform" — chamar "Form-triggered Calls" / "External Form Webhook".

- [x] 🆕 `POST /v1/webhook/typeform/call-dispatch` — dispatch call from external form

### Auth Utility

- [x] 🆕 `POST /v1/auth/identify` — identify token type (env vs system) — **decidir se entra na doc** (utility para SDK)

---

## 🔵 User Session — `auth:sanctum`

> Endpoints chamados pelo dashboard com sessão de usuário. Considerar se viram "Account API" ou ficam fora da doc pública.

### User API Tokens (PAT)
- [ ] 🆕 `GET /v1/user/api-tokens` — list user tokens
- [ ] 🆕 `POST /v1/user/api-tokens` — create token
- [ ] 🆕 `DELETE /v1/user/api-tokens/{tokenId}` — revoke token
- [ ] 🆕 `GET /user` — current user

### Credits (provavelmente só dashboard)
- [ ] 🆕 `POST /v1/credits/purchase` — purchase credits
- [x] 🆕 `POST /v1/credits/use` — use credits
- [ ] 🆕 `GET /v1/credits/balance` — balance

---

### Health & Public utility
- [ ] ⚠️ `GET /v1/health` — pode expor publicamente como `/health` simples (decidir)


## ⚠️ Páginas atuais a revisar/remover

- [ ] ⚠️ `make-external-call.mdx` — remover (rota não existe mais; expõe websocket interno)
- [ ] ⚠️ `websocket-connection.mdx` — revisar se hostnames `{us|br|eu}-agent.app.talkover.ai` devem mesmo ser públicos; se sim, remover regiões e usar host neutro
- [ ] ⚠️ `agent-trainings.mdx` (overview) — duplica os 3 .mdx específicos; consolidar
- [ ] ⚠️ `agent-actions.mdx` (overview) — duplica os 3 .mdx específicos; consolidar
- [ ] ⚠️ `make-call.mdx` — documenta 2 paths num só arquivo (agent + campaign); separar
- [ ] ⚠️ `agents.mdx` — overview gigante que documenta `/calling`, `/publish`, `/unpublish` que não têm página dedicada; extrair

---

## 🏷️ Rebrand Talkover → Talkover

- [ ] Renomear `Talkover` / `talkover` em **104 arquivos / 594 ocorrências**
- [ ] Variantes: `talkover`, `Talkover`, `TALKOVER`, `app.talkover.ai`, `talq_<token>` (decidir se prefixo de token também muda)
- [ ] Diretório `pt-br/` espelhado (mesmo conteúdo, fazer rename junto)
- [ ] Arquivos não-docs: `docs.json`, `MULTI_LANGUAGE_GUIDE.md`, `README.md`, `introduction.mdx` (raiz + locales)

---

## ✅ Próximos passos depois de marcar

1. Pegar tudo `[x]` em 🟢 PÚBLICO → escrever/atualizar `.mdx` no padrão de `endpoints/`
2. Pegar tudo `[x]` em 🔵 SESSÃO → decidir se vira "Account API" ou fica em doc separada interna
3. Confirmar com backend: range de `conversation_speed`, bug `dd()` em `cloneTemplateIntoAgent`, se `template-statistics` é admin
4. Executar rebrand Talkover → Talkover em PR isolada
