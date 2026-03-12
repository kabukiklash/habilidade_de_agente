import sqlite3
import json

db_path = "C:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/core/database/evolution.db"
conn = sqlite3.connect(db_path)
cursor = conn.execute("SELECT event_type, payload_raw, justification FROM audit_ledger ORDER BY id DESC LIMIT 10")
rows = cursor.fetchall()

print(f"--- Audit Ledger (Last 10 events) ---")
for row in rows:
    print(f"Type: {row[0]}")
    print(f"Justification: {row[2]}")
    print(f"Payload: {row[1]}")
    print("-" * 20)
conn.close()
