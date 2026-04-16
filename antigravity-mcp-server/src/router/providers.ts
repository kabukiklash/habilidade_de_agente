/**
 * LLM Router — Provider Registry
 *
 * All providers use OpenAI-compatible chat/completions endpoints.
 * API keys are read from environment variables — never hardcoded.
 *
 * Strategy mapping:
 *   fast      → Groq   (low latency, llama3)
 *   balanced  → Kimi / MiniMax (cost-effective, strong reasoning)
 *   quality   → Inception (Mercury, high capability)
 */

export type ProviderName = "groq" | "inception" | "kimi" | "minimax" | "openai" | "pollinations" | "zhipu";
export type RoutingStrategy = "fast" | "balanced" | "quality" | "engineering";

export interface ProviderConfig {
  name: ProviderName;
  baseUrl: string;
  apiKeyEnv: string;
  defaultModel: string;
  maxTokens: number;
  timeoutMs: number;
}

export const PROVIDERS: Record<ProviderName, ProviderConfig> = {
  groq: {
    name: "groq",
    baseUrl: "https://api.groq.com/openai/v1",
    apiKeyEnv: "GROQ_API_KEY",
    defaultModel: "llama-3.1-8b-instant",
    maxTokens: 2048,
    timeoutMs: 15_000,
  },
  inception: {
    name: "inception",
    baseUrl: "https://api.inceptionlabs.ai/v1",
    apiKeyEnv: "INCEPTION_API_KEY",
    defaultModel: "mercury-2",
    maxTokens: 2048,
    timeoutMs: 45_000,
  },
  kimi: {
    name: "kimi",
    baseUrl: "https://api.moonshot.ai/v1",
    apiKeyEnv: "MOONSHOT_API_KEY",
    defaultModel: "moonshot-v1-8k",
    maxTokens: 2048,
    timeoutMs: 30_000,
  },
  minimax: {
    name: "minimax",
    baseUrl: "https://api.minimax.chat/v1",
    apiKeyEnv: "MINIMAX_API_KEY",
    defaultModel: "abab6.5s-chat",
    maxTokens: 2048,
    timeoutMs: 30_000,
  },
  openai: {
    name: "openai",
    baseUrl: "https://api.openai.com/v1",
    apiKeyEnv: "OPENAI_API_KEY",
    defaultModel: "gpt-4o-mini",
    maxTokens: 2048,
    timeoutMs: 30_000,
  },
  pollinations: {
    name: "pollinations",
    baseUrl: "https://text.pollinations.ai/openai",
    apiKeyEnv: "",           // sem chave — acesso público gratuito
    defaultModel: "openai-fast",
    maxTokens: 2048,
    timeoutMs: 30_000,
  },
  zhipu: {
    name: "zhipu",
    baseUrl: "https://open.bigmodel.cn/api/paas/v4",
    apiKeyEnv: "ZHIPU_API_KEY",
    defaultModel: "glm-4.7-flash",  // gratuito; glm-4.7 / glm-5-turbo / glm-5.1 requerem saldo
    maxTokens: 4096,
    timeoutMs: 45_000,
  },
};

// Strategy → ordered list of providers (first = primary, rest = fallbacks)
// Providers ativos confirmados: OpenAI, Inception, Pollinations, Zhipu (Z.ai)
// Providers instáveis/inativos ficam no fim: Kimi (fetch failed intermitente), MiniMax (chave inválida), Groq (sem chave)
export const STRATEGY_MAP: Record<RoutingStrategy, ProviderName[]> = {
  fast:        ["pollinations", "openai",    "zhipu",     "inception", "groq",    "kimi",   "minimax"],
  balanced:    ["openai",       "inception", "pollinations", "zhipu",  "kimi",    "minimax", "groq"],
  quality:     ["inception",    "openai",    "zhipu",     "pollinations", "kimi", "minimax", "groq"],
  engineering: ["zhipu",        "inception", "openai",    "pollinations", "kimi", "minimax", "groq"],
};

export function resolveProviderChain(
  strategy: RoutingStrategy,
  forceProvider?: ProviderName,
): ProviderName[] {
  if (forceProvider) return [forceProvider];
  return STRATEGY_MAP[strategy];
}

export function getApiKey(provider: ProviderConfig): string | null {
  return process.env[provider.apiKeyEnv] ?? null;
}
