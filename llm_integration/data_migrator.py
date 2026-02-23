import os
import json
import sqlite3
from ledger_manager import LedgerManager

class DataMigrator:
    """
    Antigravity Data Migrator: JSON Legacy -> SQLite Ledger.
    Ensures technical memory is preserved during system upgrades.
    """
    def __init__(self, ledger: LedgerManager):
        self.ledger = ledger

    def migrate_directory(self, json_dir: str):
        if not os.path.exists(json_dir):
            print(f"[!] Directory not found: {json_dir}")
            return

        print(f"[*] Starting migration from: {json_dir}")
        for filename in os.listdir(json_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(json_dir, filename)
                self.migrate_file(file_path)

    def migrate_file(self, file_path: str):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            correlation_id = data.get("id", os.path.basename(file_path))
            messages = data.get("messages", [])
            
            for msg in messages:
                event_type = "LEGACY_MESSAGE"
                payload = {
                    "role": msg.get("role"),
                    "content": msg.get("content"),
                    "timestamp": msg.get("timestamp")
                }
                
                self.ledger.record_event(
                    event_type=event_type,
                    payload=payload,
                    justification="Migração de histórico legado (JSON).",
                    correlation_id=correlation_id,
                    actor="LEGACY_CONVERSATION"
                )
            print(f"[+] Migrated: {file_path}")
        except Exception as e:
            print(f"[!] Failed to migrate {file_path}: {str(e)}")

if __name__ == "__main__":
    from .ledger_manager import LedgerManager
    
    # Usage Example
    ledger = LedgerManager()
    migrator = DataMigrator(ledger)
    
    # Target directory for legacy conversations (adjust as needed)
    legacy_dir = "C:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/data/conversations"
    migrator.migrate_directory(legacy_dir)
