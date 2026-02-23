---
description: Automatically check and sync new Antigravity capabilities.
---

# Workflow: /evolve

This workflow ensures the Antigravity system remains up-to-date with its latest "Clawd-Inspired" evolutions.

## Steps

1. **Verify Index**: Read `.agent/memory/index.json`.
2. **Scan Skills**: List `.agent/skills/` to detect new modules.
3. **Register**: Update the system map in `ARCHITECTURE.md` if any new skill is missing.
4. **Notify**: Inform the user about the new "Power Level" reached.

## Triggering

Run this whenever you add a new skill to the toolkit.
