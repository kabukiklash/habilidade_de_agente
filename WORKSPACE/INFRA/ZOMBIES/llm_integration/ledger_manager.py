import sqlite3
import json
import hashlib
import hmac
import uuid
import os
import sys
import socket
from datetime import datetime
from typing import Optional, Dict, Any, List

class LedgerManager:
    """
    Antigravity Platform-Grade Ledger Manager.
    Features: Append-Only (Triggers), Canonical Payloads (Deterministic), HMAC Signatures.
    """
    def __init__(self, db_path: str = "C:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/antigravity.db"):
        self.db_path = db_path
        self.secret_key = os.environ.get("ANTIGRAVITY_LEDGER_KEY", "default_insecure_key_change_me")
        self.session_id = str(uuid.uuid4())
        self.host_id = socket.gethostname()
        self.process_id = os.getpid()
        self._initialize_db()

    def _initialize_db(self):
        with sqlite3.connect(self.db_path) as conn:
            # Check for migration needs
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='audit_ledger'")
            table_exists = cursor.fetchone()

            if table_exists:
                # Check for v2 columns
                cursor = conn.execute("PRAGMA table_info(audit_ledger)")
                columns = [col[1] for col in cursor.fetchall()]
                if "payload_c14n" not in columns:
                    self._migrate_to_v2(conn)
                
                # Check for v3 (Token Economy) columns
                cursor = conn.execute("PRAGMA table_info(audit_ledger)")
                columns = [col[1] for col in cursor.fetchall()]
                if "tokens_used" not in columns:
                    self._migrate_to_v3(conn)
            else:
                self._create_schema_latest(conn)

    def _create_schema_latest(self, conn):
        conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT UNIQUE,
                correlation_id TEXT,
                session_id TEXT,
                host_id TEXT,
                process_id INTEGER,
                actor_id TEXT,
                event_type TEXT,
                payload_raw TEXT,
                payload_c14n TEXT,
                payload_hash TEXT,
                justification TEXT,
                tokens_used INTEGER DEFAULT 0,
                tokens_saved INTEGER DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                prev_hash TEXT,
                current_hash TEXT,
                sig TEXT
            )
        """)
        
        # Enforce Append-Only via Triggers
        conn.execute("DROP TRIGGER IF EXISTS ledger_no_update")
        conn.execute("""
            CREATE TRIGGER ledger_no_update
            BEFORE UPDATE ON audit_ledger
            BEGIN
                SELECT RAISE(ABORT, 'LEDGER_APPEND_ONLY_VIOLATION: Updates prohibited.');
            END;
        """)
        
        conn.execute("DROP TRIGGER IF EXISTS ledger_no_delete")
        conn.execute("""
            CREATE TRIGGER ledger_no_delete
            BEFORE DELETE ON audit_ledger
            BEGIN
                SELECT RAISE(ABORT, 'LEDGER_APPEND_ONLY_VIOLATION: Deletions prohibited.');
            END;
        """)
        conn.commit()

    def _migrate_to_v2(self, conn):
        print("[*] Migrating Antigravity Ledger to v2 (Platform-Grade)...", file=sys.stderr)
        conn.execute("ALTER TABLE audit_ledger RENAME TO audit_ledger_old")
        self._create_schema_latest(conn)
        
        cursor = conn.execute("SELECT id, event_id, correlation_id, event_type, payload, justification, actor, timestamp, prev_hash, current_hash FROM audit_ledger_old ORDER BY id ASC")
        rows = cursor.fetchall()
        
        prev_hash = "GENESIS_BLOCK_00000000000000000000000000000000"
        for row in rows:
            old_id, event_id, correlation_id, event_type, payload_json, justification, actor, timestamp, old_prev_hash, old_current_hash = row
            
            # Reconstruct v2 fields
            payload_dict = json.loads(payload_json)
            c14n = self._canonicalize_json(payload_dict)
            p_hash = hashlib.sha256(c14n.encode("utf-8")).hexdigest()
            
            # Re-calculate hashes for v2
            current_hash_base = f"{event_id}{p_hash}{prev_hash}".encode("utf-8")
            current_hash = hashlib.sha256(current_hash_base).hexdigest()
            sig = hmac.new(self.secret_key.encode("utf-8"), current_hash.encode("utf-8"), hashlib.sha256).hexdigest()

            conn.execute("""
                INSERT INTO audit_ledger 
                (event_id, correlation_id, session_id, host_id, process_id, actor_id, event_type, payload_raw, payload_c14n, payload_hash, justification, timestamp, prev_hash, current_hash, sig)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (event_id, correlation_id, "LEGACY_SESSION", "LEGACY_HOST", 0, actor, event_type, payload_json, c14n, p_hash, justification, timestamp, prev_hash, current_hash, sig))
            
            prev_hash = current_hash
        
        conn.execute("DROP TABLE audit_ledger_old")
        conn.commit()
        print("[+] Migration completed successfully.", file=sys.stderr)

    def _migrate_to_v3(self, conn):
        print("[*] Migrating Antigravity Ledger to v3 (Token Economy)...", file=sys.stderr)
        try:
            conn.execute("ALTER TABLE audit_ledger ADD COLUMN tokens_used INTEGER DEFAULT 0")
            conn.execute("ALTER TABLE audit_ledger ADD COLUMN tokens_saved INTEGER DEFAULT 0")
            conn.commit()
            print("[+] Token Economy columns added successfully.", file=sys.stderr)
        except sqlite3.OperationalError as e:
            print(f"[!] Migration to v3 failed/skipped (already exists?): {e}", file=sys.stderr)

    def _canonicalize_json(self, data: Dict[str, Any]) -> str:
        return json.dumps(data, sort_keys=True, separators=(',', ':'))

    def record_event(self, event_type: str, payload: Dict[str, Any], justification: str, correlation_id: Optional[str] = None, actor_id: str = "ANTIGRAVITY", tokens_used: int = 0, tokens_saved: int = 0):
        event_id = str(uuid.uuid4())
        
        # 1. Canonicalization
        payload_c14n = self._canonicalize_json(payload)
        payload_hash = hashlib.sha256(payload_c14n.encode("utf-8")).hexdigest()
        payload_raw = json.dumps(payload)

        with sqlite3.connect(self.db_path) as conn:
            # 2. Hash Chain
            cursor = conn.execute("SELECT current_hash FROM audit_ledger ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            prev_hash = row[0] if row else "GENESIS_BLOCK_00000000000000000000000000000000"
            
            # 3. Current Hash calculation (event_id + payload_hash + prev_hash)
            current_hash_base = f"{event_id}{payload_hash}{prev_hash}".encode("utf-8")
            current_hash = hashlib.sha256(current_hash_base).hexdigest()
            
            # 4. Signature (HMAC)
            sig = hmac.new(self.secret_key.encode("utf-8"), current_hash.encode("utf-8"), hashlib.sha256).hexdigest()
            
            conn.execute("""
                INSERT INTO audit_ledger 
                (event_id, correlation_id, session_id, host_id, process_id, actor_id, event_type, payload_raw, payload_c14n, payload_hash, justification, tokens_used, tokens_saved, prev_hash, current_hash, sig)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (event_id, correlation_id, self.session_id, self.host_id, self.process_id, actor_id, event_type, payload_raw, payload_c14n, payload_hash, justification, tokens_used, tokens_saved, prev_hash, current_hash, sig))
            conn.commit()
            return event_id

    def verify_integrity(self) -> Dict[str, Any]:
        report = {"status": "OK", "total_events": 0, "violations": []}
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id, event_id, payload_c14n, payload_hash, prev_hash, current_hash, sig FROM audit_ledger ORDER BY id ASC")
            rows = cursor.fetchall()
            report["total_events"] = len(rows)
            
            expected_prev_hash = "GENESIS_BLOCK_00000000000000000000000000000000"
            for row in rows:
                row_id, event_id, c14n, p_hash_stored, prev_h, curr_h, sig_stored = row
                
                # Check Hash Chain
                if prev_h != expected_prev_hash:
                    report["status"] = "CORRUPTED"
                    report["violations"].append({"id": row_id, "type": "CHAIN_BROKEN", "event_id": event_id})
                    return report

                # Check Payload Determinism
                computed_p_hash = hashlib.sha256(c14n.encode("utf-8")).hexdigest()
                if computed_p_hash != p_hash_stored:
                    report["status"] = "CORRUPTED"
                    report["violations"].append({"id": row_id, "type": "PAYLOAD_TAMPERED", "event_id": event_id})
                    return report

                # Check Current Hash integrity
                recomputed_curr_h = hashlib.sha256(f"{event_id}{computed_p_hash}{prev_h}".encode("utf-8")).hexdigest()
                if recomputed_curr_h != curr_h:
                    report["status"] = "CORRUPTED"
                    report["violations"].append({"id": row_id, "type": "HASH_MISMATCH", "event_id": event_id})
                    return report

                # Check Signature
                expected_sig = hmac.new(self.secret_key.encode("utf-8"), curr_h.encode("utf-8"), hashlib.sha256).hexdigest()
                if expected_sig != sig_stored:
                    report["status"] = "UNAUTHORIZED_ALTERATION"
                    report["violations"].append({"id": row_id, "type": "SIG_INVALID", "event_id": event_id})
                    return report
                
                expected_prev_hash = curr_h
        
        return report

if __name__ == "__main__":
    # Integration Test Mode
    if "--test" in sys.argv:
        print("[*] Running Ledger v2 Platform-Grade Integrity Test...")
        manager = LedgerManager()
        
        # 1. Test record
        eid = manager.record_event("TEST", {"key": "value", "abc": 123}, "Justification for testing.")
        print(f"[+] Record OK: {eid}")
        
        # 2. Verify OK
        res = manager.verify_integrity()
        print(f"[+] Integrity Check: {res['status']}")
        
        # 3. Test Append-Only
        try:
            with sqlite3.connect(manager.db_path) as conn:
                conn.execute("UPDATE audit_ledger SET actor_id = 'HACKER' WHERE event_id = ?", (eid,))
            print("[!] FAIL: Update allowed!")
        except sqlite3.Error as e:
            print(f"[+] Append-Only (Update) Enforced: {e}")

        try:
            with sqlite3.connect(manager.db_path) as conn:
                conn.execute("DELETE FROM audit_ledger WHERE event_id = ?", (eid,))
            print("[!] FAIL: Delete allowed!")
        except sqlite3.Error as e:
            print(f"[+] Append-Only (Delete) Enforced: {e}")
            
        sys.exit(0)

    # CLI Output for Boot
    manager = LedgerManager()
    audit = manager.verify_integrity()
    print(json.dumps(audit, indent=2))
