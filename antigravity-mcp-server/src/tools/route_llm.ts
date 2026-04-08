/**
 * Tool: route_llm
 *
 * Routes a prompt to the best available external LLM based on strategy.
 * Use this to offload tasks to cheaper/faster models while Claude orchestrates.
 *
 * Strategies:
 *   fast     → Groq / llama3        (lowest latency, ~50ms)
 *   balanced → Kimi / MiniMax  (cost-efficient, strong reasoning)
 *   quality  → Inception / mercury  (highest capability)
 *
 * Output is automatically sanitized against prompt injection before
 * being returned to Claude.
 */

import { routeLLM } from "../router/llm_router.js";
import type { ProviderName, RoutingStrategy } from "../router/providers.js";

export async function routeLlmTool(params: unknown): Promise<object> {
  const p = params as Record<string, unknown>;

  const prompt = p.prompt as string | undefined;
  if (!prompt || typeof prompt !== "string" || prompt.trim().length === 0) {
    return { error: "INVALID_INPUT", reason: "prompt is required and must be a non-empty string" };
  }

  const strategy = (p.strategy as RoutingStrategy | undefined) ?? "balanced";
  const validStrategies: RoutingStrategy[] = ["fast", "balanced", "quality"];
  if (!validStrategies.includes(strategy)) {
    return { error: "INVALID_INPUT", reason: `strategy must be one of: ${validStrategies.join(", ")}` };
  }

  const validProviders: ProviderName[] = ["groq", "inception", "kimi", "minimax", "openai", "pollinations"];
  const forceProvider = p.provider as ProviderName | undefined;
  if (forceProvider && !validProviders.includes(forceProvider)) {
    return { error: "INVALID_INPUT", reason: `provider must be one of: ${validProviders.join(", ")}` };
  }

  const maxTokens = typeof p.max_tokens === "number" ? p.max_tokens : undefined;
  const temperature = typeof p.temperature === "number" ? p.temperature : undefined;
  const system  = typeof p.system   === "string" ? p.system   : undefined;
  const action  = typeof p.action   === "string" ? p.action   : undefined;
  const sessionId = typeof p.session_id === "string" ? p.session_id : undefined;

  try {
    const result = await routeLLM({
      prompt,
      system,
      strategy,
      provider: forceProvider,
      maxTokens,
      temperature,
      action,
      sessionId,
    });

    return {
      status:        "ok",
      provider_used: result.provider_used,
      model:         result.model,
      strategy_used: strategy,
      content:       result.content,
      tokens_in:     result.tokens_in,
      tokens_out:    result.tokens_out,
      latency_ms:    result.latency_ms,
      sanitized:     result.sanitized,
      warnings:      result.warnings,
      fallback_used: result.fallback_used,
      friction:      result.friction
        ? { score: result.friction.score, state: result.friction.state,
            explanation: result.friction.explanation }
        : undefined,
    };
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    return { error: "ROUTER_FAILED", reason: message };
  }
}
