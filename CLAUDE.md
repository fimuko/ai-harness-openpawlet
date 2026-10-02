# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

`ai-harness-openpawlet` is a deployable test stack for OpenPawlet, a nanobot
fork with a FastAPI console and an embedded agent runtime. There is no custom
agent code here. The repo is a container image, a config template and
compose. The design and the upstream findings are in
[`docs/architecture.md`](docs/architecture.md).

Sibling repos: `ai-harness-nanobot` (the nanobot + Langfuse counterpart),
`ai-llm-inference-service` (vLLM, :8200), `ai-requests-router` (LiteLLM,
:8401), `ml-task-api-base-shared-code` (shared Makefile, required).

### Repository Layout

```
ai-harness-openpawlet/
├── docs/architecture.md        # What OpenPawlet is, config rendering, known gaps
├── dpl/compose/
│   ├── Makefile                # shared base include + task targets
│   ├── compose.yml
│   ├── compose.{docker,podman}.cpu-override.yml
│   ├── compose.bwrap-override.yml   # added when OPENPAWLET_EXEC_SANDBOX=bwrap
│   └── envs/.env.example       # .env.dev.local is gitignored (live secrets)
├── src/openpawlet/
│   ├── Containerfile
│   ├── config.json             # template with ${VAR} refs
│   └── seed_config.py          # renders it at first start (see architecture.md)
└── data/openpawlet/            # runtime state incl. API key (gitignored)
```

## Build & Run

All commands run from `dpl/compose/`: `make init-env`, `make deploy`,
`make smoke`, `make logs`, `make reset-config`, `make down`.

## Conventions

- The OpenPawlet version is pinned (`OPENPAWLET_VERSION`, PyPI). Bump
  deliberately and re-run `make reset-config && make smoke`, because the
  provider-migration behaviour that `seed_config.py` works around may change.
- Port 8620, loopback only. The API is unauthenticated.
- Python on the host goes through `uv` (never bare `python3`).
