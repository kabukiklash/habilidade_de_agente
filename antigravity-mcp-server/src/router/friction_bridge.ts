/**
 * Friction Bridge — TypeScript → Python Per-Friction Engine
 *
 * Calls friction_check.py via spawnSync and returns a structured result.
 * If the friction engine is unavailable, fails open (STABLE) so the router
 * continues normally — friction is advisory, not a hard gate here.
 */

import { spawnSync } from "child_process";

const FRICTION_CHECK_PATH =
  "C:/Users/RobsonSilva-AfixGraf/claude-cognitive-kit/friction_check.py";

const PROJECT = "Habilidade_de_agente";

export type FrictionState = "STABLE" | "UNCERTAIN" | "HIGH_FRICTION" | "BLOCKED";

export interface FrictionResult {
  score:        number;
  state:        FrictionState;
  can_proceed:  boolean;
  needs_confirm: boolean;
  is_blocked:   boolean;
  explanation:  string;
  sources:      Record<string, number>;
  error?:       string;
}

const FALLBACK: FrictionResult = {
  score: 0.0,
  state: "STABLE",
  can_proceed: true,
  needs_confirm: false,
  is_blocked: false,
  explanation: "friction engine unavailable — proceeding",
  sources: {},
};

export function checkFriction(action: string, sessionId?: string): FrictionResult {
  const payload = JSON.stringify({ project: PROJECT, action, session_id: sessionId ?? null });

  const result = spawnSync(
    "python",
    [FRICTION_CHECK_PATH],
    { input: payload, encoding: "utf-8", timeout: 5_000 },
  );

  if (result.error || result.status !== 0) {
    return { ...FALLBACK, error: result.stderr?.slice(0, 200) || "spawn failed" };
  }

  try {
    return JSON.parse(result.stdout) as FrictionResult;
  } catch {
    return { ...FALLBACK, error: "invalid JSON from friction_check.py" };
  }
}

/**
 * Maps friction state to a routing strategy override.
 * Returns null if no override is needed (caller uses its own strategy).
 */
export function frictionToStrategy(state: FrictionState): "fast" | "balanced" | "quality" | null {
  switch (state) {
    case "STABLE":       return "quality";    // ação segura → melhor modelo
    case "UNCERTAIN":    return "balanced";   // dúvida → modelo padrão
    case "HIGH_FRICTION": return "fast";      // risco → modelo barato, economiza antes de confirmar
    case "BLOCKED":      return null;         // bloqueado → router não deve prosseguir
  }
}
