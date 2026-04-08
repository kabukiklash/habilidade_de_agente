/**
 * Circuit Breaker — Protects the CMS from cascade failures.
 *
 * States:
 *   CLOSED   → Normal operation, requests pass through.
 *   OPEN     → CMS is down, requests fail immediately with fallback.
 *   HALF     → Testing recovery: one probe request is allowed.
 */

import { config } from "../config.js";

type BreakerState = "CLOSED" | "OPEN" | "HALF";

let state: BreakerState = "CLOSED";
let failures = 0;
let openedAt: number | null = null;

export function getBreakerState(): BreakerState {
  if (state === "OPEN" && openedAt !== null) {
    const elapsed = Date.now() - openedAt;
    if (elapsed >= config.circuitBreaker.resetAfterMs) {
      state = "HALF";
    }
  }
  return state;
}

export function recordSuccess(): void {
  failures = 0;
  state = "CLOSED";
  openedAt = null;
}

export function recordFailure(): void {
  failures++;
  if (failures >= config.circuitBreaker.failureThreshold) {
    state = "OPEN";
    openedAt = Date.now();
  }
}

export function isAvailable(): boolean {
  const current = getBreakerState();
  return current === "CLOSED" || current === "HALF";
}

export function breakerStatus(): object {
  return { state: getBreakerState(), failures, openedAt };
}
