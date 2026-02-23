---
name: knowledge-vault
description: Persistent memory management across sessions. Allows agents to store, retrieve, and summarize architectural decisions and past learnings.
tools: Read, Write, Grep
---

# Knowledge Vault Skill

This skill provides a structured way to maintain state across different chat sessions.

## Storage Protocol

- All memory files are stored in `.agent/memory/`.
- Use JSON for structured data (schema/versioning).
- Use Markdown for narrative history and ADRs (Architecture Decision Records).

## Core Responsibilities

1. **Write Context**: Save current project state, chosen tech stack, and resolved bugs.
2. **Search Memory**: Use grep to find past solutions to similar problems.
3. **Prune**: Keep memory relevant by summarizing old entries.

## Usage

When starting a new session, the `historian` agent should use this skill to load relevant context.
