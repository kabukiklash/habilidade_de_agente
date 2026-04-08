/**
 * Antigravity MCP Server — Configuration
 * Reads from environment, never hardcoded in production.
 */

export const config = {
  cms: {
    baseUrl: process.env.CMS_BASE_URL ?? "http://localhost:8090",
    apiKey:  process.env.CMS_API_KEY  ?? "ace-genesis-sovereign-key-2026",
    timeoutMs: parseInt(process.env.CMS_TIMEOUT_MS ?? "5000", 10),
  },
  dedup: {
    // Similarity threshold: if word-overlap score >= this value, reject as duplicate
    threshold: parseFloat(process.env.DEDUP_THRESHOLD ?? "0.75"),
    // How many results to fetch when checking for duplicates
    topK: parseInt(process.env.DEDUP_TOP_K ?? "3", 10),
  },
  loopGuard: {
    maxSearchPerSession:    parseInt(process.env.LG_MAX_SEARCH    ?? "50", 10),
    maxStorePerSession:     parseInt(process.env.LG_MAX_STORE     ?? "10", 10),
    maxDecisionPerSession:  parseInt(process.env.LG_MAX_DECISION  ?? "5",  10),
    maxEventPerSession:     parseInt(process.env.LG_MAX_EVENT     ?? "20", 10),
  },
  circuitBreaker: {
    failureThreshold: parseInt(process.env.CB_FAILURE_THRESHOLD ?? "3",     10),
    resetAfterMs:     parseInt(process.env.CB_RESET_AFTER_MS    ?? "30000", 10),
  },
  actor: process.env.CMS_ACTOR ?? "claude-mcp-server",
};
