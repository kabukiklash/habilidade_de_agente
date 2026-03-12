import sqlite3

db_path = "C:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/core/database/evolution.db"
conn = sqlite3.connect(db_path)

try:
    conn.execute("ALTER TABLE audit_ledger ADD COLUMN tokens_saved INTEGER DEFAULT 0")
    print("Column tokens_saved added.")
except sqlite3.OperationalError:
    print("Column tokens_saved already exists.")

try:
    conn.execute("ALTER TABLE audit_ledger ADD COLUMN usd_saved REAL DEFAULT 0.0")
    print("Column usd_saved added.")
except sqlite3.OperationalError:
    print("Column usd_saved already exists.")

conn.commit()
conn.close()
print("Migration completed.")
