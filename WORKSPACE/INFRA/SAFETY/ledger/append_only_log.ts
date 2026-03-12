import * as crypto from 'crypto';
import * as fs from 'fs';

/**
 * AppendOnlyLedger v0
 * Proporciona um log imutável e encadeado por hash para auditoria do Moltbot.
 */

export interface LedgerEntry {
    index: number;
    timestamp: string;
    intent_id: string;
    event_type: string;
    payload: any;
    prev_hash: string;
    hash: string;
    signature?: string;
}

export class AppendOnlyLedger {
    private logPath: string;
    private secret: string = "ANTIGRAVITY_SAFETY_SECRET_2026"; // Em produção, carregar de env

    constructor(logPath: string) {
        this.logPath = logPath;
        if (!fs.existsSync(this.logPath)) {
            fs.writeFileSync(this.logPath, JSON.stringify([]));
        }
    }

    private calculateHash(entry: Partial<LedgerEntry>): string {
        const data = `${entry.index}${entry.timestamp}${entry.intent_id}${entry.event_type}${JSON.stringify(entry.payload)}${entry.prev_hash}`;
        return crypto.createHash('sha256').update(data).digest('hex');
    }

    private sign(hash: string): string {
        return crypto.createHmac('sha256', this.secret).update(hash).digest('hex');
    }

    public append(intent_id: string, event_type: string, payload: any): LedgerEntry {
        const log = this.readLog();
        const prevEntry = log[log.length - 1];
        const index = log.length;
        const timestamp = new Date().toISOString();
        const prev_hash = prevEntry ? prevEntry.hash : "0".repeat(64);

        const entry: Partial<LedgerEntry> = {
            index,
            timestamp,
            intent_id,
            event_type,
            payload,
            prev_hash
        };

        const hash = this.calculateHash(entry);
        const signature = this.sign(hash);

        const fullEntry: LedgerEntry = { ...entry as LedgerEntry, hash, signature };

        log.push(fullEntry);
        fs.writeFileSync(this.logPath, JSON.stringify(log, null, 2));

        return fullEntry;
    }

    private readLog(): LedgerEntry[] {
        const data = fs.readFileSync(this.logPath, 'utf8');
        return JSON.parse(data);
    }

    public verifyIntegrity(): boolean {
        const log = this.readLog();
        for (let i = 0; i < log.length; i++) {
            const entry = log[i];
            const prevHash = i === 0 ? "0".repeat(64) : log[i - 1].hash;

            // Check chaining
            if (entry.prev_hash !== prevHash) return false;

            // Check hash
            const recomputedHash = this.calculateHash(entry);
            if (entry.hash !== recomputedHash) return false;

            // Check signature
            if (entry.signature !== this.sign(entry.hash)) return false;
        }
        return true;
    }
}
