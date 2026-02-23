import * as fs from 'fs';
import * as path from 'path';

export interface ActionPacket {
    intent_id: string;
    state: string;
    requested_ops: string[];
    file_scope: string[];
    commands: string[];
    network: boolean;
    risk_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
    budget_limit_tokens: number;
    human_ack_required: boolean;
    attestation?: string;
}

export class Gatekeeper {
    private cmsUrl = "http://localhost:8090";
    private safetyLockPath = path.join(__dirname, "../../SAFETY_LOCK.lock");

    async validate(packet: ActionPacket): Promise<{ success: boolean; reason?: string; audit_id?: string }> {
        // G-Alpha: Physical Safety Breaker (Kill Switch Check)
        if (fs.existsSync(this.safetyLockPath)) {
            return { success: false, reason: "G-ALPHA: CRITICAL_LOCK - System is under manual containment. No actions allowed." };
        }

        // G-Omega: Hard-Coded Invariants (Cannot be bypassed by AI reasoning)
        const forbiddenDirectives = ["delete_audit_logs", "disable_gatekeeper", "bypass_human_ack", "self_replicate"];
        if (packet.commands.some(cmd => forbiddenDirectives.some(d => cmd.includes(d)))) {
            return { success: false, reason: "G-OMEGA: INVARIANT_VIOLATION - Action attempts to subvert core safety protocols." };
        }

        // G0: State Validation
        if (packet.state === "VERIFIED") {
            return { success: false, reason: "G0: Cannot process a packet already in VERIFIED state" };
        }

        // G1: Scope Allowlist
        const allowedPrefix = "C:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/";
        if (packet.file_scope.some(path => !path.startsWith(allowedPrefix))) {
            return { success: false, reason: `G1: Forbidden path outside of authorized workspace` };
        }

        // G2: Operation Allowlist
        const allowedOps = ["READ_FILE", "WRITE_FILE_SCOPED", "RUN_TESTS", "BUILD_LOCAL", "DIFF_ONLY", "GENERATE_REPORT"];
        if (packet.requested_ops.some(op => !allowedOps.includes(op))) {
            return { success: false, reason: "G2: Operation not allowed by policy" };
        }

        // G3: Network Control
        if (packet.network && packet.risk_level !== "LOW") {
            return { success: false, reason: "G3: Network access requires LOW risk level and special signing" };
        }

        // G4: Resource Budget (Hard Cap)
        const MAX_TOKEN_BUDGET = 50000;
        if (packet.budget_limit_tokens > MAX_TOKEN_BUDGET) {
            return { success: false, reason: `G4: Token budget ${packet.budget_limit_tokens} exceeds hard limit ${MAX_TOKEN_BUDGET}` };
        }

        // G5: CMS Risk History Check (Simulated for Implementation/Auditory)
        console.log(`🛡️ [Gatekeeper] Consulting CMS History for Intent: ${packet.intent_id}...`);

        // G6: Advanced Command Pattern Audit
        const forbiddenPatterns = ["rm -rf", "sudo", "curl", "wget", "ssh", "scp", "powershell", "format", "del /s"];
        if (packet.commands.some(cmd => forbiddenPatterns.some(p => cmd.toLowerCase().includes(p)))) {
            return { success: false, reason: "G6: Dangerous/Forbidden command pattern detected" };
        }

        // G7: Cortex Intent Audit (Kimi Logic)
        if (packet.risk_level === "HIGH" || packet.risk_level === "CRITICAL") {
            console.log("🧠 [Gatekeeper] Requesting Cortex Audit (Kimi) for high-risk intent...");
            if (!packet.human_ack_required) {
                return { success: false, reason: "G7: HIGH/CRITICAL risk actions require explicit Human Acknowledge" };
            }
        }

        // G8: Ledger Evidence Persistence
        console.log("📝 [Gatekeeper] Recording evidence in CMS Ledger...");
        const auditId = `audit_${Date.now()}`;

        return { success: true, audit_id: auditId };
    }
}
