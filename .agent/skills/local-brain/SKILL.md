---
name: local-brain
description: Integration with local AI models via LM Studio (compatible with OpenAI API). Delegates heavy code generation and logic tasks to local hardware to save tokens.
tools: run_command, Write
---

# Local Brain Skill

This skill allows the agent to offload tasks to a local LLM running on the user's machine.

## Configuration

- **Endpoint**: `https://fees-str-producers-binary.trycloudflare.com` (Dynamically updated)
- **API Standard**: OpenAI Compatible (`/v1/chat/completions`)
- **Models**:
  - `code-beast` (Qwen2.5-Coder-7B)
  - `logic-beast` (Llama-3.1-8B)
  - `creative-beast` (Mistral-Nemo-12B)

## Usage Categories

1. **Code Generation**: Writing repetitive boilerplate, unit tests, or refactoring large files.
2. **Drafting**: Creating documentation drafts, READMEs, or marketing copy.
3. **Reasoning**: Analyzing complex logical problems or brainstorming architecture options.

## Execution Protocol (Python Script)

Use the provided `ask_local.py` script to send prompts to the local model.
Usage: `python .agent/skills/local-brain/scripts/ask_local.py --model <model_alias> --prompt "<your_prompt>"`
