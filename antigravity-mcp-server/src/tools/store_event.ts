/**
 * Tool: store_event
 * Records system events in the Antigravity CMS event log.
 */

import { appendEvent, CmsUnavailableError } from "../gateway/cms_client.js";
import { validateStoreEvent } from "../gateway/ace.js";
import { checkAndIncrement } from "../gateway/loop_guard.js";

export async function storeEvent(params: unknown): Promise<object> {
  // 1. ACE validation
  const aceResult = validateStoreEvent(params);
  if (!aceResult.valid) {
    return { error: "ACE_REJECTED", reason: aceResult.reason };
  }

  // 2. LoopGuard
  const guard = checkAndIncrement("store_event");
  if (!guard.allowed) {
    return {
      error:  "LOOP_GUARD",
      reason: `store_event limit reached (${guard.limit}/session).`,
    };
  }

  const p = params as Record<string, unknown>;

  // 3. Write to CMS
  try {
    const response = await appendEvent(
      (p.event_type as string).toUpperCase(),
      {
        description: p.description,
        ...(p.payload as object ?? {}),
      },
      p.description as string,
    );

    return {
      status:     "stored",
      event_id:   response.event_id,
      created_at: response.created_at,
      event_type: p.event_type,
      _guard: { call: guard.count, limit: guard.limit },
    };
  } catch (err) {
    if (err instanceof CmsUnavailableError) {
      return { error: "CMS_UNAVAILABLE", reason: err.message, fallback: true };
    }
    return { error: "UNEXPECTED", reason: (err as Error).message };
  }
}
