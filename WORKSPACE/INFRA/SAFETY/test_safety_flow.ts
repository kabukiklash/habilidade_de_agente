/**
 * Moltbot Safety Test Script
 * Cycles a packet through the state machine: PREFLIGHT -> APPROVED -> EXECUTING -> VERIFIED
 */

import { ActionPacket, Gatekeeper } from './gatekeeper/validator';
import { Executor } from './executor_stub/run_packet';
import { generateProof } from './executor_stub/generate_proof';
import { AppendOnlyLedger } from './ledger/append_only_log';

async function testFlow() {
    const ledger = new AppendOnlyLedger('./moltbot_safety/ledger/audit.json');
    console.log("🛠️ Starting Safety Flow Test...");

    const packet: ActionPacket = {
        intent_id: "TEST-CMD-001",
        state: "PREFLIGHT",
        requested_ops: ["WRITE_FILE_SCOPED"],
        file_scope: ["/workspace/genesiscore/moltbot_safety/test.log"],
        commands: ["touch /workspace/genesiscore/moltbot_safety/test.log"],
        network: false,
        risk_level: "LOW",
        human_ack_required: false
    };

    // 1. Validation
    const gatekeeper = new Gatekeeper();
    const validation = gatekeeper.validate(packet);

    if (validation.success) {
        console.log("✅ G0-G6 Validation PASS");
        packet.state = "APPROVED"; // Transition
    } else {
        console.log(`❌ Validation FAIL: ${validation.reason}`);
        return;
    }

    // 2. Execution
    const executor = new Executor();
    try {
        await executor.run(packet);
        packet.state = "PROOF_READY";
    } catch (e) {
        console.error(`❌ Execution Error: ${e}`);
        return;
    }

    // 3. Proof
    const proof = generateProof(packet.intent_id, true);
    console.log("📄 ProofBundle Generated:", proof.status);

    packet.state = "VERIFIED";
    console.log("🏁 Final State: VERIFIED");

    // 4. Ledger Check
    const integrity = ledger.verifyIntegrity();
    console.log("🛡️ Ledger Integrity Check:", integrity ? "VALID" : "TAMPERED");
}

testFlow();
