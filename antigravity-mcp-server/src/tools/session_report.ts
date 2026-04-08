/**
 * Tool: session_report
 * Consulta o CMS e retorna relatório de eficiência da sessão atual.
 * Compara tokens estimados vs tokens economizados pelo cache/memória.
 */

import { config } from "../config.js";

interface ResponseEvent {
  id: string;
  payload: {
    tokens_input?: number;
    tokens_output?: number;
    cost_usd?: number;
    cache_hits?: number;
    topic?: string;
  };
  timestamp: string;
}

async function fetchSessionEvents(): Promise<ResponseEvent[]> {
  try {
    const res = await fetch(`${config.cms.baseUrl}/tables/events`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-ACE-API-KEY": config.cms.apiKey,
      },
      body: JSON.stringify({
        filters: { event_type: "CLAUDE_RESPONSE" },
        sort: "created_at DESC",
        limit: 100,
      }),
    });
    if (!res.ok) return [];
    const data = await res.json() as { data: ResponseEvent[] };
    return data.data ?? [];
  } catch {
    return [];
  }
}

async function fetchCmsGlobalStats(): Promise<{
  tokens_used: number;
  tokens_saved: number;
  efficiency_percent: number;
} | null> {
  try {
    const res = await fetch(`${config.cms.baseUrl}/tables/events/stats`, {
      headers: { "X-ACE-API-KEY": config.cms.apiKey },
    });
    if (!res.ok) return null;
    return await res.json() as { tokens_used: number; tokens_saved: number; efficiency_percent: number };
  } catch {
    return null;
  }
}

export async function sessionReport(params: unknown): Promise<object> {
  const p = (params ?? {}) as Record<string, unknown>;
  const showGlobal = p.include_global !== false;

  const [events, globalStats] = await Promise.all([
    fetchSessionEvents(),
    showGlobal ? fetchCmsGlobalStats() : Promise.resolve(null),
  ]);

  // ── Aggregate session metrics ──────────────────────────────────────────
  let totalInput    = 0;
  let totalOutput   = 0;
  let totalCostUsd  = 0;
  let totalCacheHits = 0;
  const topics: string[] = [];

  for (const ev of events) {
    const pl = ev.payload ?? {};
    totalInput    += pl.tokens_input  ?? 0;
    totalOutput   += pl.tokens_output ?? 0;
    totalCostUsd  += pl.cost_usd      ?? 0;
    totalCacheHits += pl.cache_hits   ?? 0;
    if (pl.topic) topics.push(pl.topic);
  }

  const totalTokens = totalInput + totalOutput;

  // Cost without cache (if every input had to be re-read from scratch)
  const savedByCache    = totalCacheHits * 1200; // avg ~1200 tokens per cache hit
  const costWithoutInfra = ((totalInput + savedByCache) * 3 + totalOutput * 15) / 1_000_000;
  const actualCost      = (totalInput * 3 + totalOutput * 15) / 1_000_000;
  const savedUsd        = costWithoutInfra - actualCost;
  const efficiencyPct   = costWithoutInfra > 0
    ? ((savedUsd / costWithoutInfra) * 100).toFixed(1)
    : "0.0";

  const report: Record<string, unknown> = {
    status: "ok",
    session: {
      responses_tracked: events.length,
      tokens_input:       totalInput,
      tokens_output:      totalOutput,
      tokens_total:       totalTokens,
      cache_hits:         totalCacheHits,
      tokens_saved_by_cache: savedByCache,
      cost_usd_actual:    parseFloat(actualCost.toFixed(4)),
      cost_usd_without_infra: parseFloat(costWithoutInfra.toFixed(4)),
      saved_usd:          parseFloat(savedUsd.toFixed(4)),
      efficiency_percent: parseFloat(efficiencyPct),
      topics_covered:     topics,
    },
  };

  if (globalStats) {
    report.antigravity_global = {
      tokens_used:       globalStats.tokens_used,
      tokens_saved:      globalStats.tokens_saved,
      efficiency_percent: globalStats.efficiency_percent,
    };
  }

  return report;
}
