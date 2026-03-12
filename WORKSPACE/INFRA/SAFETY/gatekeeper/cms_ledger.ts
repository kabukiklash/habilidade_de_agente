/**
 * CMS Ledger Helper: Interface for Moltbot Safety -> CMS
 */

import axios from 'axios';

export interface AuditRecord {
    intent_id: string;
    risk_level: string;
    gate_results: Record<string, any>;
    timestamp: string;
    decision: "ALLOWED" | "REJECTED";
}

export class CMSLedger {
    private readonly cmsUrl = "http://localhost:8090";

    async recordSafetyEvent(record: AuditRecord): Promise<void> {
        console.log(`📡 [CMSLedger] Sending Audit Record for Intent: ${record.intent_id}...`);

        try {
            // Append to CMS via the events API
            await axios.post(`${this.cmsUrl}/tables/events/append`, {
                event_type: "SAFETY_AUDIT",
                actor: "MOLTBOT_GATEKEEPER",
                payload: record,
                justification: `Safety validation for intent ${record.intent_id}: Result ${record.decision}`
            });

            console.log("✅ [CMSLedger] Audit recorded successfully.");
        } catch (error) {
            console.error("❌ [CMSLedger] Failed to record audit in CMS:", (error as Error).message);
            // In a production scenario, we would fallback to local SQLite here
        }
    }

    async checkRiskHistory(targetId: string): Promise<any> {
        // Implementation of G5: Querying past events for risk correlation
        try {
            const response = await axios.post(`${this.cmsUrl}/memory/query`, {
                query_text: `Safety history for ${targetId}`
            });
            return response.data;
        } catch (error) {
            return null;
        }
    }
}
