# Architecture

_Date: 2026-10-02 · OpenPawlet 0.4.1_

## What OpenPawlet is

OpenPawlet (`open-pawlet` on PyPI) is a **renamed fork of nanobot** (HKUDS),
taken around April 2026. It keeps the same module layout and docstrings, with
`nanobot` renamed to `openpawlet`, and does not credit the original project.
It adds a FastAPI console (dashboard with token/cost charts, sessions,
channels, MCP, cron) and runs the agent runtime inside the same process on
one port.

It does **not** wrap nanobot, and it does **not** create a throwaway container
per task. Like nanobot, it can sandbox each shell command with bubblewrap
inside its own container.

The nanobot counterpart, with Langfuse, is `ai-harness-nanobot`.

| | OpenPawlet (this repo) | nanobot (`ai-harness-nanobot`) |
|---|---|---|
| Upstream | JackLuguibin/OpenPawlet, small (≈100★), last release May 2026 | HKUDS/nanobot, very active (0.3.5, Sep 2026) |
| UI | Console: dashboard, usage/cost charts, sessions, channels, MCP, cron | WebUI: chat, settings, model presets, apps, automations |
| Auth | **None**: the API is unauthenticated | WebUI password |
| Models | One provider in config, more can be added in the console | Named presets, switched live |
| Tracing | None (usage charts in the console only) | Langfuse built in |

## Layout

```
 browser ──► 127.0.0.1:8620  OpenPawlet (console + REST + /v1 + agent runtime)
                                   │
                                   ├─► per-command bwrap sandbox (optional)
                                   ▼
     host.containers.internal ─┬─ :8200  ai-llm-inference-service (vLLM)   provider: vllm
                               └─ :8401  ai-requests-router (LiteLLM)      provider: custom
     internet ─────────────────┬─ OpenRouter                               provider: openrouter
                               └─ Claude API                               provider: anthropic
```

## Config rendering

OpenPawlet uses the older nanobot config schema (`agents.defaults.provider` +
`model`). On first boot it migrates `providers.*` into its own
`workspace/llm_providers.json`. That migration has two problems:

- It doesn't resolve `${VAR}` refs.
- Without a model hint it makes the **first** provider block the default, and
  ignores `agents.defaults.provider`.

So `src/openpawlet/seed_config.py` renders the config at first start: env refs
resolved, and only the selected provider kept. As a result, **the real API key
sits on disk** in `data/openpawlet/` (gitignored). After changing the provider
or keys: `make reset-config`.

## Requirements on the local model

The same as for nanobot. vLLM needs tool calling
(`--enable-auto-tool-choice --tool-call-parser hermes` for Qwen3) and ≥16k
context, set through `VLLM_EXTRA_FLAGS` / `VLLM_MAX_MODEL_LEN` in the
inference service's env file.

## Known gaps

- **No auth**: anyone who can reach the port controls the agent. Keep it on
  loopback, or put an authenticating reverse proxy in front.
- **Upstream risk**: a small single-maintainer fork that trails nanobot's
  fixes and features.
- **No egress control**: bwrap isolates the filesystem, not the network.
- **Tool loops on small models**: Qwen3-4B sometimes "answers" by calling the
  `message` tool over and over instead of finishing the turn. The template caps
  `maxToolIterations` at 20 (upstream default: 200) so such a turn ends in
  seconds instead of running for many minutes. `make smoke` uses a fresh
  session each run, so earlier pongs in the history don't feed the loop.
