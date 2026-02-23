/**
 * Executor Stub: run_packet.ts
 * Only runs if packet state is APPROVED and passes Gatekeeper.
 */

import { ActionPacket } from '../gatekeeper/validator';
import { Gatekeeper } from '../gatekeeper/validator';
import { AppendOnlyLedger } from '../ledger/append_only_log';

export class Executor {
    private gatekeeper = new Gatekeeper();
    private ledger = new AppendOnlyLedger('./moltbot_safety/ledger/audit.json');

    async run(packet: ActionPacket) {
        // Audit entrance
        this.ledger.append(packet.intent_id, "EXECUTION_ATTEMPT", { state: packet.state });

        if (packet.state !== "APPROVED") {
            this.ledger.append(packet.intent_id, "EXECUTION_REJECTED", { reason: "Packet is not APPROVED" });
            throw new Error("Executor: Packet state must be APPROVED to run.");
        }

        const validation = this.gatekeeper.validate(packet);
        if (!validation.success) {
            this.ledger.append(packet.intent_id, "EXECUTION_REJECTED", { reason: validation.reason });
            throw new Error(`Executor: Gatekeeper rejected packet: ${validation.reason}`);
        }

        // SIMULATION OF EXECUTION
        console.log(`🚀 Executing Intent ${packet.intent_id}...`);
        this.ledger.append(packet.intent_id, "EXECUTION_START", { commands: packet.commands });

        // Mock execution
        const results = packet.commands.map(cmd => ({ command: cmd, status: "OK" }));

        this.ledger.append(packet.intent_id, "EXECUTION_COMPLETE", { results });
        return results;
    }
}
