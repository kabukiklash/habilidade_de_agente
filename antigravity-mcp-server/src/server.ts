/**
 * Antigravity MCP Server
 * Exposes 6 tools to Claude via Model Context Protocol (stdio transport).
 *
 * Tools:
 *   - search_memory  → CMS /memory/query
 *   - store_memory   → CMS /audits/append  (with dedup)
 *   - log_decision   → CMS /tables/events/append
 *   - store_event    → CMS /tables/events/append
 *   - log_response   → CMS CLAUDE_RESPONSE event (token/cost tracking)
 *   - session_report → Efficiency report from CMS history
 *
 * Architecture:
 *   Claude → MCP Server → ACE → LoopGuard → [Dedup] → Breaker → CMS
 */

import { Server }         from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

import { searchMemory }  from "./tools/search_memory.js";
import { storeMemory }   from "./tools/store_memory.js";
import { logDecision }   from "./tools/log_decision.js";
import { storeEvent }    from "./tools/store_event.js";
import { logResponse }   from "./tools/log_response.js";
import { sessionReport } from "./tools/session_report.js";
import { readFileSmart } from "./tools/read_file_smart.js";
import { routeLlmTool } from "./tools/route_llm.js";
import { resetSession, getCounters } from "./gateway/loop_guard.js";
import { breakerStatus } from "./gateway/breaker.js";
import { appendEvent }  from "./gateway/cms_client.js";
import { config }       from "./config.js";

// ─── Server definition ───────────────────────────────────────────────────────

const server = new Server(
  { name: "antigravity-mcp", version: "1.0.0" },
  { capabilities: { tools: {} } },
);

// ─── Tool registry ───────────────────────────────────────────────────────────

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "search_memory",
      description:
        "Semantic search on Antigravity CMS. Use to retrieve relevant context before responding. " +
        "Returns facts, artifacts and concepts matching the query.",
      inputSchema: {
        type: "object",
        properties: {
          query: {
            type: "string",
            description: "The search query text (semantic, not keyword-only)",
          },
          top_k: {
            type: "number",
            description: "Number of results to return (1–20, default 5)",
          },
        },
        required: ["query"],
      },
    },
    {
      name: "store_memory",
      description:
        "Persist a valuable piece of knowledge to the Antigravity CMS. " +
        "Only use for: decisions, bugs, patterns, rules, constraints, or context. " +
        "Do NOT use for intermediate thoughts or redundant summaries. " +
        "Deduplication runs automatically — duplicates are rejected.",
      inputSchema: {
        type: "object",
        properties: {
          content: {
            type: "string",
            description: "The knowledge to persist (20–4000 chars)",
          },
          type: {
            type: "string",
            enum: ["decision", "bug", "pattern", "rule", "constraint", "context"],
            description: "Category of this memory",
          },
          metadata: {
            type: "object",
            description: "Optional: { project, module, confidence, tags[] }",
          },
        },
        required: ["content", "type"],
      },
    },
    {
      name: "log_decision",
      description:
        "Record an important architectural or technical decision with its justification.",
      inputSchema: {
        type: "object",
        properties: {
          decision: {
            type: "string",
            description: "What was decided (min 10 chars)",
          },
          context: {
            type: "string",
            description: "Why this decision was made (min 10 chars)",
          },
          alternatives: {
            type: "array",
            items: { type: "string" },
            description: "Options that were considered but rejected",
          },
          impact: {
            type: "string",
            enum: ["high", "medium", "low"],
            description: "Impact level of this decision",
          },
        },
        required: ["decision", "context", "impact"],
      },
    },
    {
      name: "store_event",
      description:
        "Record a system event in the Antigravity CMS event log (session_start, error, milestone, etc).",
      inputSchema: {
        type: "object",
        properties: {
          event_type: {
            type: "string",
            description: "Event type (e.g. SESSION_START, ERROR, MILESTONE)",
          },
          description: {
            type: "string",
            description: "Human-readable description of the event",
          },
          payload: {
            type: "object",
            description: "Optional structured data about the event",
          },
        },
        required: ["event_type", "description"],
      },
    },
    {
      name: "log_response",
      description:
        "Register token consumption and cost for this Claude response. " +
        "Call at the END of each response with estimated token counts. " +
        "Used to build session efficiency reports.",
      inputSchema: {
        type: "object",
        properties: {
          tokens_input: {
            type: "number",
            description: "Estimated input tokens for this response",
          },
          tokens_output: {
            type: "number",
            description: "Estimated output tokens for this response",
          },
          cache_hits: {
            type: "number",
            description: "Number of times cache avoided re-reading files",
          },
          topic: {
            type: "string",
            description: "Short description of what this response was about",
          },
        },
        required: ["tokens_input", "tokens_output"],
      },
    },
    {
      name: "session_report",
      description:
        "Returns full efficiency report: tokens used, tokens saved by cache, " +
        "cost in USD, and Antigravity global stats. Call when user asks about cost or efficiency.",
      inputSchema: {
        type: "object",
        properties: {
          include_global: {
            type: "boolean",
            description: "Include Antigravity global CMS stats (default: true)",
          },
        },
      },
    },
    {
      name: "read_file_smart",
      description:
        "Read a file with automatic compression for large files. " +
        "USE THIS INSTEAD OF the Read tool when a file is large (> 120 lines) or when the " +
        "PreToolUse hook says '[LARGE FILE — use read_file_smart]'. " +
        "Returns full content for small files. For large files, returns a compressed skeleton " +
        "(imports, class/def signatures) saving 30–60% of tokens. " +
        "Does NOT require CMS to be running.",
      inputSchema: {
        type: "object",
        properties: {
          file_path: {
            type: "string",
            description: "Absolute path to the file to read",
          },
          max_lines: {
            type: "number",
            description:
              "Lines threshold above which compression is applied (default: 120)",
          },
        },
        required: ["file_path"],
      },
    },
    {
      name: "route_llm",
      description:
        "Route a prompt to the best available external LLM based on a strategy. " +
        "Use to offload tasks to cheaper/faster models while Claude orchestrates. " +
        "Strategies: fast=Groq/llama3, balanced=Kimi/MiniMax, quality=Inception/Mercury. " +
        "Output is automatically sanitized against prompt injection.",
      inputSchema: {
        type: "object",
        properties: {
          prompt: {
            type: "string",
            description: "The prompt to send to the external LLM",
          },
          system: {
            type: "string",
            description: "Optional system message for the LLM",
          },
          strategy: {
            type: "string",
            enum: ["fast", "balanced", "quality"],
            description: "Routing strategy (default: balanced)",
          },
          provider: {
            type: "string",
            enum: ["groq", "inception", "kimi", "minimax", "openai", "pollinations"],
            description: "Force a specific provider (overrides strategy)",
          },
          max_tokens: {
            type: "number",
            description: "Maximum tokens in the response (default: 2048)",
          },
          temperature: {
            type: "number",
            description: "Sampling temperature 0-1 (default: 0.3)",
          },
        },
        required: ["prompt"],
      },
    },
  ],
}));

// ─── Tool dispatcher ─────────────────────────────────────────────────────────

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  let result: object;

  switch (name) {
    case "search_memory":   result = await searchMemory(args);   break;
    case "store_memory":    result = await storeMemory(args);    break;
    case "log_decision":    result = await logDecision(args);    break;
    case "store_event":     result = await storeEvent(args);     break;
    case "log_response":    result = await logResponse(args);    break;
    case "session_report":  result = await sessionReport(args);  break;
    case "read_file_smart": result = await readFileSmart(args);  break;
    case "route_llm":       result = await routeLlmTool(args);    break;
    default:
      result = { error: "UNKNOWN_TOOL", reason: `Tool '${name}' not found` };
  }

  return {
    content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
  };
});

// ─── Startup ─────────────────────────────────────────────────────────────────

async function main() {
  resetSession();

  // Log session start to CMS (best-effort)
  try {
    await appendEvent("SESSION_START", {
      description: "Claude MCP session initialized",
      actor: config.actor,
      server: "antigravity-mcp-server v1.0.0",
    });
  } catch {
    // Non-fatal — session continues even if this fails
  }

  const transport = new StdioServerTransport();
  await server.connect(transport);

  process.stderr.write(
    `[antigravity-mcp] Server started | CMS: ${config.cms.baseUrl} | Actor: ${config.actor}\n`,
  );
}

main().catch((err) => {
  process.stderr.write(`[antigravity-mcp] FATAL: ${err.message}\n`);
  process.exit(1);
});
