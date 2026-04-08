/**
 * Tool: store_memory
 * Persists AI knowledge to the Antigravity CMS via /audits/append.
 * Runs deduplication check before every write.
 */

import { appendAudit, CmsUnavailableError } from "../gateway/cms_client.js";
import { validateStoreMemory } from "../gateway/ace.js";
import { checkAndIncrement } from "../gateway/loop_guard.js";
import { checkDuplicate } from "../gateway/dedup.js";

export async function storeMemory(params: unknown): Promise<object> {
  // 1. ACE validation
  const aceResult = validateStoreMemory(params);
  if (!aceResult.valid) {
    return { error: "ACE_REJECTED", reason: aceResult.reason };
  }

  // 2. LoopGuard
  const guard = checkAndIncrement("store_memory");
  if (!guard.allowed) {
    return {
      error:  "LOOP_GUARD",
      reason: `store_memory limit reached (${guard.limit}/session). Session may be looping.`,
    };
  }

  const p        = params as Record<string, unknown>;
  const content  = (p.content as string).trim();
  const type     = p.type as string;
  const metadata = (p.metadata as Record<string, unknown>) ?? {};

  // 3. Deduplication — search before write
  const dedup = await checkDuplicate(content);
  if (dedup.isDuplicate) {
    return {
      status:       "rejected_duplicate",
      reason:       `Content is too similar to existing memory (similarity: ${(dedup.similarity! * 100).toFixed(1)}%)`,
      duplicate_of: dedup.duplicateOf,
      similarity:   dedup.similarity,
    };
  }

  // 4. Build semantic translation from metadata
  const semanticTranslation = metadata.tags
    ? `type:${type} tags:${(metadata.tags as string[]).join(",")} project:${metadata.project ?? "unknown"}`
    : `type:${type} project:${metadata.project ?? "unknown"}`;

  // 5. Write to CMS
  try {
    const response = await appendAudit(
      content,
      `type:${type} | ${JSON.stringify(metadata)}`,
      type,
      semanticTranslation,
    );

    return {
      status:    "stored",
      audit_id:  response.audit_id ?? "created",
      type,
      content_preview: content.substring(0, 100) + (content.length > 100 ? "…" : ""),
      _guard: { call: guard.count, limit: guard.limit },
    };
  } catch (err) {
    if (err instanceof CmsUnavailableError) {
      return { error: "CMS_UNAVAILABLE", reason: err.message, fallback: true };
    }
    return { error: "UNEXPECTED", reason: (err as Error).message };
  }
}
