---
name: sandbox-executor
description: Secure execution of tools and commands within a Docker sandbox. Prevents host contamination and provides a controlled environment for testing.
tools: run_command
---

# Sandbox Executor Skill

This skill allows the agent to run dangerous or experimental code inside a disposable Docker container.

## Default Images

- **Node.js**: `node:slim`
- **Python**: `python:3.11-slim`
- **Shell/General**: `alpine:latest`

## Execution Protocol

1. **Prepare**: Mount only necessary files to `/workspace` inside the container.
2. **Execute**: Run `docker run --rm -v ${PWD}:/workspace -w /workspace <image> <command>`.
3. **Cleanup**: Containers are automatically removed via `--rm`.

## Usage Examples

- Testing a new npm package without installing it locally.
- Running a Python script that requires a specific version.
- Validating file system changes in a fresh environment.

## 🛑 SAFETY PROTOCOL (MANDATORY)

1. **Explicit Authorization**: You must ASK the user for permission before running ANY command in the sandbox.
2. **Review**: Show the user exactly what image and command will be run.
3. **No Auto-Run**: Never set `SafeToAutoRun` to `true` for sandbox tools unless explicitly overriding for a user-approved workflow.
