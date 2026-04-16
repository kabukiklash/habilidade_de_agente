import sqlite3
import os

db_path = r"c:\Users\RobsonSilva-AfixGraf\Habilidade_de_agente\01_COGNITIVE_MEMORY_SERVICE\database\antigravity.db"

if os.path.exists(db_path):
    print(f"\n--- Database: {os.path.basename(db_path)} ---")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables: {[t[0] for t in tables]}")
        for table in [t[0] for t in tables]:
            cursor.execute(f"SELECT count(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"Table {table}: {count} records")
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            print(f"Columns: {[c[1] for c in columns]}")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
else:
    print(f"File not found: {db_path}")
