/**
 * ACE — Access Control & Entry validation.
 * Validates all inputs BEFORE they reach the CMS.
 * Rejects malformed, empty, or oversized requests immediately.
 */

const VALID_MEMORY_TYPES = ["decision", "bug", "pattern", "rule", "constraint", "context"] as const;
type MemoryType = typeof VALID_MEMORY_TYPES[number];

export interface AceError {
  valid: false;
  reason: string;
}

export interface AceOk {
  valid: true;
}

export type AceResult = AceOk | AceError;

export function validateSearchMemory(params: unknown): AceResult {
  const p = params as Record<string, unknown>;
  if (!p.query || typeof p.query !== "string") {
    return { valid: false, reason: "query must be a non-empty string" };
  }
  if (p.query.trim().length === 0) {
    return { valid: false, reason: "query cannot be blank" };
  }
  if (typeof p.top_k !== "undefined" && (typeof p.top_k !== "number" || p.top_k < 1 || p.top_k > 20)) {
    return { valid: false, reason: "top_k must be a number between 1 and 20" };
  }
  return { valid: true };
}

export function validateStoreMemory(params: unknown): AceResult {
  const p = params as Record<string, unknown>;
  if (!p.content || typeof p.content !== "string") {
    return { valid: false, reason: "content must be a non-empty string" };
  }
  if (p.content.trim().length < 20) {
    return { valid: false, reason: "content too short (min 20 chars) — not worth persisting" };
  }
  if (p.content.length > 4000) {
    return { valid: false, reason: "content too long (max 4000 chars) — break into smaller memories" };
  }
  if (!p.type || !VALID_MEMORY_TYPES.includes(p.type as MemoryType)) {
    return { valid: false, reason: `type must be one of: ${VALID_MEMORY_TYPES.join(", ")}` };
  }
  return { valid: true };
}

export function validateLogDecision(params: unknown): AceResult {
  const p = params as Record<string, unknown>;
  if (!p.decision || typeof p.decision !== "string" || p.decision.trim().length < 10) {
    return { valid: false, reason: "decision must be a string with at least 10 characters" };
  }
  if (!p.context || typeof p.context !== "string" || p.context.trim().length < 10) {
    return { valid: false, reason: "context must be a string with at least 10 characters" };
  }
  const validImpact = ["high", "medium", "low"];
  if (!p.impact || !validImpact.includes(p.impact as string)) {
    return { valid: false, reason: `impact must be one of: ${validImpact.join(", ")}` };
  }
  return { valid: true };
}

export function validateStoreEvent(params: unknown): AceResult {
  const p = params as Record<string, unknown>;
  if (!p.event_type || typeof p.event_type !== "string" || p.event_type.trim().length === 0) {
    return { valid: false, reason: "event_type must be a non-empty string" };
  }
  if (!p.description || typeof p.description !== "string" || p.description.trim().length === 0) {
    return { valid: false, reason: "description must be a non-empty string" };
  }
  return { valid: true };
}
