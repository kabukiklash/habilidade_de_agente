/**
 * Tool: search_memory
 * Semantic search on the Antigravity CMS.
 */

import { queryMemory, CmsUnavailableError } from "../gateway/cms_client.js";
import { validateSearchMemory } from "../gateway/ace.js";
import { checkAndIncrement } from "../gateway/loop_guard.js";

export async function searchMemory(params: unknown): Promise<object> {
  // 1. ACE validation
  const aceResult = validateSearchMemory(params);
  if (!aceResult.valid) {
    return { error: "ACE_REJECTED", reason: aceResult.reason };
  }

  // 2. LoopGuard
  const guard = checkAndIncrement("search_memory");
  if (!guard.allowed) {
    return {
      error: "LOOP_GUARD",
      reason: `search_memory limit reached (${guard.limit}/session). Session may be looping.`,
    };
  }

  const p = params as Record<string, unknown>;
  const query  = p.query as string;
  const top_k  = typeof p.top_k === "number" ? p.top_k : 5;

  // 3. Call CMS
  try {
    const response = await queryMemory(query, top_k);

    const total =
      response.context.facts.length +
      response.context.artifacts.length +
      response.context.concepts.length;

    return {
      status:    "ok",
      query_id:  response.query_id,
      latency_ms: response.latency_ms,
      total_results: total,
      context: {
        facts:     response.context.facts,
        artifacts: response.context.artifacts,
        concepts:  response.context.concepts,
        explain:   response.context.explain,
      },
      _guard: { call: guard.count, limit: guard.limit },
    };
  } catch (err) {
    if (err instanceof CmsUnavailableError) {
      return {
        error:    "CMS_UNAVAILABLE",
        reason:   err.message,
        fallback: true,
      };
    }
    return { error: "UNEXPECTED", reason: (err as Error).message };
  }
}
