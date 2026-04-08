/**
 * Deduplication — Word-overlap similarity check.
 * Checks BOTH the memory graph (queryMemory) AND the recent audit history.
 * This is necessary because /audits/append stores to ai_reasoning_audits,
 * which is NOT indexed in the /memory/query knowledge graph.
 *
 * Uses Jaccard similarity on word tokens (no external deps).
 */

import { queryMemory } from "./cms_client.js";
import { config } from "../config.js";

function tokenize(text: string): Set<string> {
  return new Set(
    text
      .toLowerCase()
      .replace(/[^a-z0-9\sáéíóúàãõâêôçüñ]/gi, " ")
      .split(/\s+/)
      .filter(w => w.length > 2)
  );
}

function jaccard(a: Set<string>, b: Set<string>): number {
  if (a.size === 0 && b.size === 0) return 1;
  const intersection = new Set([...a].filter(x => b.has(x)));
  const union = new Set([...a, ...b]);
  return intersection.size / union.size;
}

function extractText(item: object): string {
  const obj = item as Record<string, unknown>;
  return [
    obj["raw_ai_learning"],
    obj["content"],
    obj["text"],
    obj["description"],
    obj["payload"],
  ]
    .filter(Boolean)
    .map(v => typeof v === "string" ? v : JSON.stringify(v))
    .join(" ");
}

export interface DedupResult {
  isDuplicate: boolean;
  similarity?: number;
  duplicateOf?: string;
}

async function fetchRecentAudits(limit = 20): Promise<object[]> {
  try {
    const res = await fetch(
      `${config.cms.baseUrl}/audits/history?limit=${limit}`,
      { headers: { "X-ACE-API-KEY": config.cms.apiKey } },
    );
    if (!res.ok) return [];
    const data = await res.json() as { data?: object[] };
    return data.data ?? [];
  } catch {
    return [];
  }
}

export async function checkDuplicate(content: string): Promise<DedupResult> {
  const contentTokens = tokenize(content);

  // ── Check 1: knowledge graph (facts, artifacts, concepts) ──────────────
  try {
    const response = await queryMemory(content, config.dedup.topK);
    const graphResults = [
      ...response.context.facts,
      ...response.context.artifacts,
      ...response.context.concepts,
    ];
    for (const item of graphResults) {
      const existingText = extractText(item);
      if (!existingText) continue;
      const similarity = jaccard(contentTokens, tokenize(existingText));
      if (similarity >= config.dedup.threshold) {
        const obj = item as Record<string, unknown>;
        const id = String(obj["id"] ?? obj["audit_id"] ?? "graph-unknown");
        return { isDuplicate: true, similarity, duplicateOf: id };
      }
    }
  } catch { /* fail-open */ }

  // ── Check 2: recent audit history (ai_reasoning_audits) ────────────────
  const audits = await fetchRecentAudits(20);
  for (const item of audits) {
    const existingText = extractText(item);
    if (!existingText) continue;
    const similarity = jaccard(contentTokens, tokenize(existingText));
    if (similarity >= config.dedup.threshold) {
      const obj = item as Record<string, unknown>;
      const id = String(obj["audit_id"] ?? "audit-unknown");
      return { isDuplicate: true, similarity, duplicateOf: id };
    }
  }

  return { isDuplicate: false };
}
