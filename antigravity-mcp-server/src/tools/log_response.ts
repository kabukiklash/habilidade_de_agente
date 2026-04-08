/**
 * Tool: log_response
 * Registra métricas de cada resposta do Claude no CMS.
 * Chamado ao final de cada resposta para acumular histórico de eficiência.
 *
 * Estimativa de tokens:
 *   - input:  contagem de palavras do prompt × 1.33
 *   - output: contagem de palavras da resposta × 1.33
 *   - cache_hits: quantas vezes o cache evitou releitura nesta resposta
 */

import { appendEvent, CmsUnavailableError } from "../gateway/cms_client.js";
import { validateStoreEvent } from "../gateway/ace.js";
import { checkAndIncrement } from "../gateway/loop_guard.js";

// Preços Claude Sonnet (USD por 1M tokens)
const PRICE_INPUT_PER_1M  = 3.00;
const PRICE_OUTPUT_PER_1M = 15.00;

function estimateCost(inputTokens: number, outputTokens: number): number {
  return (inputTokens * PRICE_INPUT_PER_1M + outputTokens * PRICE_OUTPUT_PER_1M) / 1_000_000;
}

export async function logResponse(params: unknown): Promise<object> {
  const p = (params ?? {}) as Record<string, unknown>;

  // MCP SDK may pass numbers as strings — coerce safely
  const tokensInput  = Number(p.tokens_input)  || 0;
  const tokensOutput = Number(p.tokens_output) || 0;
  const cacheHits    = Number(p.cache_hits)    || 0;
  const topic        = typeof p.topic === "string" ? p.topic : "general";

  const costUsd = estimateCost(tokensInput, tokensOutput);

  // tokens que o cache economizou (média 1200 tokens por hit)
  const tokensSavedByCache = cacheHits * 1200;
  const costSavedUsd       = estimateCost(tokensSavedByCache, 0);

  const guard = checkAndIncrement("store_event");
  if (!guard.allowed) {
    return { error: "LOOP_GUARD", reason: "store_event limit reached" };
  }

  try {
    const response = await appendEvent(
      "CLAUDE_RESPONSE",
      {
        topic,
        tokens_input:        tokensInput,
        tokens_output:       tokensOutput,
        tokens_total:        tokensInput + tokensOutput,
        cache_hits:          cacheHits,
        tokens_saved_cache:  tokensSavedByCache,
        cost_usd:            parseFloat(costUsd.toFixed(6)),
        cost_saved_usd:      parseFloat(costSavedUsd.toFixed(6)),
      },
      `Claude response on: ${topic}`,
    );

    return {
      status:       "logged",
      event_id:     response.event_id,
      tokens_input:  tokensInput,
      tokens_output: tokensOutput,
      cost_usd:      parseFloat(costUsd.toFixed(4)),
      saved_usd:     parseFloat(costSavedUsd.toFixed(4)),
      topic,
    };
  } catch (err) {
    if (err instanceof CmsUnavailableError) {
      return { error: "CMS_UNAVAILABLE", reason: err.message, fallback: true };
    }
    return { error: "UNEXPECTED", reason: (err as Error).message };
  }
}
