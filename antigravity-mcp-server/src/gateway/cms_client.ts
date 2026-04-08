/**
 * CMS Client — HTTP layer to the Antigravity CMS.
 * All calls go through the Circuit Breaker.
 * Header: X-ACE-API-KEY (confirmed from CMS security.py)
 */

import { config } from "../config.js";
import { isAvailable, recordSuccess, recordFailure } from "./breaker.js";

const BASE = config.cms.baseUrl;
const HEADERS = {
  "Content-Type": "application/json",
  "X-ACE-API-KEY": config.cms.apiKey,
};

async function cmsPost<T>(path: string, body: object): Promise<T> {
  if (!isAvailable()) {
    throw new CmsUnavailableError("Circuit Breaker is OPEN — CMS unreachable");
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), config.cms.timeoutMs);

  try {
    const res = await fetch(`${BASE}${path}`, {
      method: "POST",
      headers: HEADERS,
      body: JSON.stringify(body),
      signal: controller.signal,
    });

    if (!res.ok) {
      const text = await res.text();
      throw new CmsHttpError(res.status, text);
    }

    const data = await res.json() as T;
    recordSuccess();
    return data;
  } catch (err) {
    if (err instanceof CmsUnavailableError || err instanceof CmsHttpError) throw err;
    recordFailure();
    throw new CmsUnavailableError(`CMS request failed: ${(err as Error).message}`);
  } finally {
    clearTimeout(timer);
  }
}

// ─── Public API ──────────────────────────────────────────────────────────────

export interface MemoryQueryResponse {
  query_id: string;
  latency_ms: number;
  context: {
    facts:     object[];
    artifacts: object[];
    concepts:  object[];
    links:     object[];
    explain:   object[];
  };
}

export async function queryMemory(queryText: string, topK = 5): Promise<MemoryQueryResponse> {
  return cmsPost<MemoryQueryResponse>("/memory/query", {
    query_text:    queryText,
    requester:     config.actor,
    vector_topk:   topK,
    graph_hops:    1,
    exclude_expired: true,
  });
}

export interface AuditAppendResponse {
  audit_id?: string;
  status?:   string;
}

export async function appendAudit(
  rawLearning: string,
  eventContext: string,
  ruleApplied?: string,
  semanticTranslation?: string,
): Promise<AuditAppendResponse> {
  return cmsPost<AuditAppendResponse>("/audits/append", {
    source_node:          config.actor,
    raw_ai_learning:      rawLearning,
    event_context:        eventContext,
    rule_applied:         ruleApplied ?? null,
    semantic_translation: semanticTranslation ?? null,
  });
}

export interface EventAppendResponse {
  event_id:   string;
  created_at: string;
}

export async function appendEvent(
  eventType: string,
  payload:   object,
  justification?: string,
): Promise<EventAppendResponse> {
  return cmsPost<EventAppendResponse>("/tables/events/append", {
    event_type:    eventType,
    actor:         config.actor,
    payload,
    justification: justification ?? null,
  });
}

// ─── Errors ──────────────────────────────────────────────────────────────────

export class CmsUnavailableError extends Error {
  constructor(msg: string) { super(msg); this.name = "CmsUnavailableError"; }
}

export class CmsHttpError extends Error {
  constructor(public status: number, body: string) {
    super(`CMS HTTP ${status}: ${body}`);
    this.name = "CmsHttpError";
  }
}
