"""Seed ~/.openpawlet/config.json on first start, then exec the command.

OpenPawlet migrates providers.* into its own workspace/llm_providers.json on
first boot without resolving ${VAR} refs, and marks the first block as the
default. So the template is rendered here instead: env refs resolved and only
the selected provider (agents.defaults.provider) kept. Unlike nanobot, the
resulting file holds the real keys (data/ is gitignored).
"""

import json
import os
import re
import sys
from pathlib import Path

cfg = Path(os.environ["STACK_CONFIG_PATH"])
if not cfg.exists():
    raw = Path(os.environ["STACK_CONFIG_TEMPLATE"]).read_text()
    data = json.loads(re.sub(r"\$\{(\w+)\}", lambda m: os.environ.get(m.group(1), ""), raw))
    provider = data["agents"]["defaults"]["provider"]
    data["providers"] = {provider: data["providers"][provider]}
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(json.dumps(data, indent=2))
    print(f"[seed] wrote {cfg} (provider={provider})", flush=True)

os.execvp(sys.argv[1], sys.argv[1:])
