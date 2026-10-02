# =============================================================================
# ai-stack-openpawlet — Makefile
# =============================================================================
# OpenPawlet (console + embedded nanobot-fork runtime) on local or hosted models.
#
# Quick Start:
#   make init-env                 # Create the env file
#   make deploy                   # Deploy with the runtime set in the env file
#   make smoke                    # One agent turn through the configured provider
# =============================================================================

# ===== SHARED BASE PATTERN - DO NOT MODIFY IN CHILD REPOS =====
SHARED_DIR := ../../../ml-task-api-base-shared-code/dpl/compose-shared

include $(SHARED_DIR)/Makefile.base
include $(SHARED_DIR)/Makefile.build
# ===== END SHARED BASE PATTERN =====

.DEFAULT_GOAL := help

# ===== TASK-SPECIFIC CODE - MODIFY AS NEEDED =====

# bwrap exec sandbox needs extra container privileges (see compose.bwrap-override.yml)
_SANDBOX := $(shell grep '^OPENPAWLET_EXEC_SANDBOX=' envs/$(ENV) 2>/dev/null | head -1 | cut -d'=' -f2 | tr -d '[:space:]')
ifeq ($(_SANDBOX),bwrap)
    COMPOSE_CMD += -f compose.bwrap-override.yml
endif

# Data dir must exist (and be owned by the host user) before the bind mount
prepare:
	@mkdir -p ../../data/openpawlet

deploy: prepare

init-env: ## Create envs/$(ENV) from .env.example (never overwrites)
	@if [ -f envs/$(ENV) ]; then echo -e "$(YELLOW)envs/$(ENV) exists, leaving it alone$(NC)"; exit 0; fi; \
	cp envs/.env.example envs/$(ENV); \
	echo -e "$(GREEN)[OK] envs/$(ENV) created — set provider + key, then make deploy$(NC)"

smoke: ## Run one OpenPawlet agent turn
	@$(COMPOSE_CMD) exec -T openpawlet openpawlet agent -m "Reply with exactly: pong"

shell: ## Open a shell in the OpenPawlet container
	@$(COMPOSE_CMD) exec openpawlet /bin/bash

reset-config: ## Re-render config.json + provider store from the env file (keeps sessions + workspace)
	@rm -f ../../data/openpawlet/config.json ../../data/openpawlet/workspace/llm_providers.json
	@$(COMPOSE_CMD) up -d --force-recreate openpawlet
	@echo -e "$(GREEN)[OK] Config re-rendered$(NC)"

# ===== END TASK-SPECIFIC CODE =====
