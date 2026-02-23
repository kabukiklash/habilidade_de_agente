---
name: remote-bridge
description: Remote execution and tunneling. Allows the agent to connect to remote nodes (Linux/Android/iOS) to execute commands.
tools: run_command, Agent
---

# Remote Bridge Skill

This skill provides the capability to orchestrate tasks across different machines.

## Connection Protocol

1. **Discovery**: Look for active nodes via local network or predefined SSH hosts.
2. **Tunneling**: Establish secure tunnels using SSH or Cloudflare Tunnels (inspired by Clawdbot's Tailscale integration).
3. **Execution**: Send `run_command` payloads to the remote node.

## Usage

- Use `ssh <user>@<host> "<command>"` for direct execution.
- Use `agent` tool to delegate sub-tasks to instances running on remote nodes.

## Safety

- All remote commands should be logged in `.agent/memory/remote_logs.md`.
- No sensitive keys should be passed in plain text.
