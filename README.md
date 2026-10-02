# ai-stack-openpawlet

Deployable test stack for [OpenPawlet](https://github.com/JackLuguibin/OpenPawlet),
a nanobot fork with a web console and an embedded agent runtime, on a model
backend of your choice: local vLLM (`ai-llm-inference-service`), LiteLLM
(`ai-requests-router`), OpenRouter or the Claude API.

The nanobot + Langfuse counterpart is `ai-stack-nanobot`. How the two relate,
and the known gaps: [docs/architecture.md](docs/architecture.md).

---

## Quick start

Requires `ml-task-api-base-shared-code` as a sibling directory.

```bash
cd dpl/compose
make init-env             # envs/.env.dev.local
# Edit .env.dev.local: OPENPAWLET_PROVIDER, OPENPAWLET_MODEL and that provider's key
make deploy
make smoke                # one agent turn → "pong"
```

Console: http://127.0.0.1:8620. It has no login, so it is published on
loopback only.

## Choosing the model backend

| `OPENPAWLET_PROVIDER` | Backend | Needs |
|---|---|---|
| `vllm` | ai-llm-inference-service, host :8200 | `LOCAL_LLM_API_KEY`; vLLM with tool calling and ≥16k context |
| `custom` | ai-requests-router (LiteLLM), host :8401 | `ROUTER_API_KEY` |
| `openrouter` | OpenRouter | `OPENROUTER_API_KEY` |
| `anthropic` | Claude API | `ANTHROPIC_API_KEY` |

Set `OPENPAWLET_MODEL` to the ID that provider expects. After changing either,
run `make reset-config`. More providers can be added from the console.

## Commands (from `dpl/compose/`)

```bash
make init-env             # create the env file (never overwrites)
make deploy               # build + start
make logs                 # tail logs
make smoke                # agent turn
make reset-config         # re-render config from the env file
make shell                # shell in the container
make down                 # stop (data preserved)
```

Runtime state (config, provider store, sessions, memory, workspace) lives in
`data/openpawlet/` (gitignored, and it **contains the provider API key**).

## Security notes

- The console API is unauthenticated. Do not bind it beyond `127.0.0.1`.
- `OPENPAWLET_EXEC_SANDBOX=bwrap` runs every agent shell command in a
  bubblewrap sandbox. This adds `SYS_ADMIN` and unconfined AppArmor/seccomp to
  the container.
- The sandbox does not restrict network egress.
