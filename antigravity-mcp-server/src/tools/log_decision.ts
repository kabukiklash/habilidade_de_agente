/**
 * Tool: log_decision
 * Records architectural or important decisions in the CMS event log.
 */

import { appendEvent, CmsUnavailableError } from "../gateway/cms_client.js";
import { validateLogDecision } from "../gateway/ace.js";
import { checkAndIncrement } from "../gateway/loop_guard.js";

export async function logDecision(params: unknown): Promise<object> {
  // 1. ACE validation
  const aceResult = validateLogDecision(params);
  if (!aceResult.valid) {
    return { error: "ACE_REJECTED", reason: aceResult.reason };
  }

  // 2. LoopGuard
  const guard = checkAndIncrement("log_decision");
  if (!guard.allowed) {
    return {
      error:  "LOOP_GUARD",
      reason: `log_decision limit reached (${guard.limit}/session).`,
    };
  }

  const p = params as Record<string, unknown>;

  // 3. Write to CMS
  try {
    const response = await appendEvent(
      "DECISION",
      {
        decision:     p.decision,
        context:      p.context,
        alternatives: p.alternatives ?? [],
        impact:       p.impact,
      },
      `${p.impact?.toString().toUpperCase()} impact decision: ${p.decision}`,
    );

    return {
      status:     "logged",
      event_id:   response.event_id,
      created_at: response.created_at,
      impact:     p.impact,
      decision_preview: (p.decision as string).substring(0, 100),
      _guard: { call: guard.count, limit: guard.limit },
    };
  } catch (err) {
    if (err instanceof CmsUnavailableError) {
      return { error: "CMS_UNAVAILABLE", reason: err.message, fallback: true };
    }
    return { error: "UNEXPECTED", reason: (err as Error).message };
  }
}
