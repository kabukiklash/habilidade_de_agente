/**
 * LLM Router — Core Engine
 *
 * Routes prompts to the best available provider based on strategy.
 * All providers are OpenAI-compatible — one HTTP client handles all.
 *
 * Fallback chain: if primary provider fails (no key, timeout, API error),
 * automatically tries the next in the strategy chain.
 *
 * Returns sanitized output — safe to surface directly to Claude.
 */

import { ProviderName, RoutingStrategy, PROVIDERS, resolveProviderChain, getApiKey } from "./providers.js";
import { sanitizeOutput, SanitizeResult }  from "./output_sanitizer.js";
import { checkFriction, frictionToStrategy, FrictionResult } from "./friction_bridge.js";

export interface RouterRequest {
  prompt: string;
  system?: string;
  strategy?: RoutingStrategy;
  provider?: ProviderName;
  maxTokens?: number;
  temperature?: number;
  action?: string;       // descrição da ação para o friction check
  sessionId?: string;
}

export interface RouterResponse {
  provider_used: ProviderName;
  model: string;
  content: string;
  tokens_in: number;
  tokens_out: number;
  latency_ms: number;
  sanitized: boolean;
  warnings: string[];
  fallback_used: boolean;
  friction?: FrictionResult;
}

interface OpenAICompletionResponse {
  choices: Array<{ message: { content: string } }>;
  usage?: { prompt_tokens: number; completion_tokens: number };
  model?: string;
}

async function callProvider(
  providerName: ProviderName,
  request: RouterRequest,
): Promise<RouterResponse> {
  const cfg = PROVIDERS[providerName];
  const apiKey = getApiKey(cfg);
  const requiresKey = cfg.apiKeyEnv !== "";

  if (requiresKey && !apiKey) {
    throw new Error(`NO_API_KEY: ${cfg.apiKeyEnv} not set for provider=${providerName}`);
  }

  const messages: Array<{ role: string; content: string }> = [];
  if (request.system) {
    messages.push({ role: "system", content: request.system });
  }
  messages.push({ role: "user", content: request.prompt });

  const payload = {
    model:       cfg.defaultModel,
    messages,
    max_tokens:  request.maxTokens ?? cfg.maxTokens,
    temperature: request.temperature ?? 0.3,
  };

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), cfg.timeoutMs);
  const t0 = Date.now();

  let raw: OpenAICompletionResponse;
  try {
    const res = await fetch(`${cfg.baseUrl}/chat/completions`, {
      method:  "POST",
      headers: {
        ...(apiKey ? { "Authorization": `Bearer ${apiKey}` } : {}),
        "Content-Type":  "application/json",
      },
      body:   JSON.stringify(payload),
      signal: controller.signal,
    });

    if (!res.ok) {
      const body = await res.text().catch(() => "");
      throw new Error(`HTTP_${res.status}: ${body.slice(0, 200)}`);
    }

    raw = (await res.json()) as OpenAICompletionResponse;
  } finally {
    clearTimeout(timer);
  }

  const latency_ms = Date.now() - t0;
  const rawContent = raw.choices?.[0]?.message?.content ?? "";
  const sanitized: SanitizeResult = sanitizeOutput(rawContent, providerName);

  return {
    provider_used: providerName,
    model:         raw.model ?? cfg.defaultModel,
    content:       sanitized.content,
    tokens_in:     raw.usage?.prompt_tokens     ?? 0,
    tokens_out:    raw.usage?.completion_tokens ?? 0,
    latency_ms,
    sanitized:     !sanitized.safe,
    warnings:      sanitized.warnings,
    fallback_used: false,
  };
}

export async function routeLLM(request: RouterRequest): Promise<RouterResponse> {
  // Per-Friction check — ajusta estratégia baseado no risco semântico da ação
  const action = request.action ?? request.prompt.slice(0, 120);
  const friction = checkFriction(action, request.sessionId);

  if (friction.is_blocked) {
    throw new Error(`FRICTION_BLOCKED: ${friction.explanation}`);
  }

  // Friction pode sobrescrever a estratégia (a menos que provider seja forçado)
  let effectiveStrategy: RoutingStrategy = request.strategy ?? "balanced";
  if (!request.provider && !request.strategy) {
    const frictionStrategy = frictionToStrategy(friction.state);
    if (frictionStrategy) effectiveStrategy = frictionStrategy;
  }

  const chain = resolveProviderChain(effectiveStrategy, request.provider);

  let lastError: Error | null = null;

  for (let i = 0; i < chain.length; i++) {
    const providerName = chain[i];
    try {
      const result = await callProvider(providerName, request);
      result.fallback_used = i > 0;
      result.friction = friction;
      return result;
    } catch (err) {
      lastError = err instanceof Error ? err : new Error(String(err));
      // NO_API_KEY → skip silently to next; other errors → log and try next
      const reason = lastError.message.startsWith("NO_API_KEY") ? "no_key" : "error";
      process.stderr.write(
        `[LLMRouter] provider=${providerName} skipped reason=${reason}: ${lastError.message.slice(0, 120)}\n`,
      );
    }
  }

  throw new Error(
    `LLMRouter: all providers failed for strategy=${effectiveStrategy}. Last error: ${lastError?.message ?? "unknown"}`,
  );
}
