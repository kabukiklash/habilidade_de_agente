# ADR-006: Antigravity Containment Protocol (Safety Breaker)

## Status
Proposed (Request by User: "Safety beyond the word")

## Context
The integration of advanced reasoning models (Kimi k2.5) and autonomous execution capabilities (Moltbot) introduces a non-zero risk of "Agency" (unintended autonomous behavior). To ensure the user retains absolute control, a multi-layered containment mechanism is required to paralyze the system instantly if an anomaly is detected.

## Proposed Decision
Implement a "Safety Breaker" system consisting of three levels of containment:

1.  **Level 1: Logical Lock (G-Alpha)**:
    - A new gate in `validator.ts` that checks for the existence of `SAFETY_LOCK.lock`.
    - If present, ALL `ActionPackets` are rejected immediately with status `CRITICAL_LOCK`.

2.  **Level 2: Process Purge (Kill Switch)**:
    - A standalone script `EMERGENCY_KILL.bat` that terminates all Antigravity-related processes (Node, Python, Docker containers, Tunnels).
    - This is the "Nuclear Option" to be used if the logical gates are bypassed.

3.  **Level 3: Hard-Coded Invariants**:
    - A set of "Forbidden Intents" that cannot be authorized by Kimi or any other model. These are hard-coded in the TypeScript source and require manual code changes to be removed.

## Expectations
- **Instant Response**: Recovery from `Agency` detection to system paralysis must take < 500ms.
- **User Ownership**: Only the human user can reset the logical lock by manually deleting the lock file.

## Reference
Implementation will be added to `Habilidade_de_agente/moltbot_safety/`.
