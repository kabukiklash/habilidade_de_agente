/**
 * LoopGuard — Prevents Claude from calling tools in runaway loops.
 * Tracks call counts per session. Resets when a new session is detected.
 */

import { config } from "../config.js";

type ToolName = "search_memory" | "store_memory" | "log_decision" | "store_event";

const limits: Record<ToolName, number> = {
  search_memory: config.loopGuard.maxSearchPerSession,
  store_memory:  config.loopGuard.maxStorePerSession,
  log_decision:  config.loopGuard.maxDecisionPerSession,
  store_event:   config.loopGuard.maxEventPerSession,
};

const counters: Record<ToolName, number> = {
  search_memory: 0,
  store_memory:  0,
  log_decision:  0,
  store_event:   0,
};

/** Returns true if the tool call is allowed, false if limit is reached. */
export function checkAndIncrement(tool: ToolName): { allowed: boolean; count: number; limit: number } {
  const count = counters[tool];
  const limit = limits[tool];

  if (count >= limit) {
    return { allowed: false, count, limit };
  }

  counters[tool]++;
  return { allowed: true, count: counters[tool], limit };
}

/** Reset all counters (call at session start). */
export function resetSession(): void {
  (Object.keys(counters) as ToolName[]).forEach(k => { counters[k] = 0; });
}

export function getCounters(): Record<ToolName, { count: number; limit: number }> {
  return (Object.keys(counters) as ToolName[]).reduce((acc, k) => {
    acc[k] = { count: counters[k], limit: limits[k] };
    return acc;
  }, {} as Record<ToolName, { count: number; limit: number }>);
}
