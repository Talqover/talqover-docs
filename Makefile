# Talkover docs — build & quality targets.
#
# Common usage:
#   make help          # list targets
#   make check         # editorial health check
#   make pdfs          # all PDFs (talkover + every client × en + pt-br)
#   make pdf-acme      # just Acme (en + pt-br)
#   make pdf-acme-en   # just Acme EN
#   make clean         # remove dist/

# ----- Discover clients automatically from clients/*.json --------------------
# Excludes _template.json. Adding a new client is `cp _template.json foo.json`.

CLIENTS := $(filter-out _template,$(notdir $(basename $(wildcard clients/*.json))))

# ----- Default ---------------------------------------------------------------

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Talkover docs — make targets"
	@echo ""
	@echo "  make check                    Run editorial health check"
	@echo "  make pdfs                     Build ALL PDFs (talkover + every client × en + pt-br)"
	@echo ""
	@echo "  make pdf-talkover             Build Talkover (en + pt-br)"
	@echo "  make pdf-talkover-en          Build Talkover EN"
	@echo "  make pdf-talkover-pt-br       Build Talkover pt-BR"
	@echo ""
	@echo "  Per-client targets (auto-discovered from clients/*.json):"
	@for c in $(CLIENTS); do \
	  echo "  make pdf-$$c           Build $$c (en + pt-br)"; \
	  echo "  make pdf-$$c-en        Build $$c EN"; \
	  echo "  make pdf-$$c-pt-br     Build $$c pt-BR"; \
	done
	@echo ""
	@echo "  make clients                  List clients found in clients/"
	@echo "  make rebrand-check            Verify whitelabel PDFs have 0 talqover/talkover refs"
	@echo "  make clean                    Remove dist/"

# ----- Editorial -------------------------------------------------------------

.PHONY: check
check:
	@bash editorial/check.sh

# ----- PDF builds ------------------------------------------------------------

dist:
	@mkdir -p dist

# --- Talkover (default brand) ---
.PHONY: pdf-talkover pdf-talkover-en pdf-talkover-pt-br
pdf-talkover: pdf-talkover-en pdf-talkover-pt-br

pdf-talkover-en: | dist
	@python3 tools/gen_pdf.py --lang en

pdf-talkover-pt-br: | dist
	@python3 tools/gen_pdf.py --lang pt-br

# --- Per-client targets ---
# Generated explicitly per discovered client to avoid pattern-rule collisions
# with `pdf-talkover-*` and to give clean error messages if a client name typos.

# Build per-client en
define _client_target_en
.PHONY: pdf-$(1)-en
pdf-$(1)-en: | dist
	@python3 tools/gen_pdf.py --client clients/$(1).json --lang en
endef

# Build per-client pt-br
define _client_target_pt
.PHONY: pdf-$(1)-pt-br
pdf-$(1)-pt-br: | dist
	@python3 tools/gen_pdf.py --client clients/$(1).json --lang pt-br
endef

# Aggregate "pdf-<client>" -> both languages
define _client_aggregate
.PHONY: pdf-$(1)
pdf-$(1): pdf-$(1)-en pdf-$(1)-pt-br
endef

$(foreach c,$(CLIENTS),$(eval $(call _client_target_en,$(c))))
$(foreach c,$(CLIENTS),$(eval $(call _client_target_pt,$(c))))
$(foreach c,$(CLIENTS),$(eval $(call _client_aggregate,$(c))))

# --- All PDFs ---
.PHONY: pdfs
pdfs: pdf-talkover $(foreach c,$(CLIENTS),pdf-$(c))
	@echo ""
	@echo "All PDFs built:"
	@ls -1 dist/*.pdf

# ----- Helpers ---------------------------------------------------------------

.PHONY: clients
clients:
	@echo "talkover (default)"
	@for c in $(CLIENTS); do echo "$$c"; done

.PHONY: clean
clean:
	@rm -rf dist/

.PHONY: rebrand-check
rebrand-check:
	@python3 editorial/rebrand_check.py
