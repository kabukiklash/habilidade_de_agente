import sqlite3
import os

dbs = [
    r"c:\Users\RobsonSilva-AfixGraf\Habilidade_de_agente\01_COGNITIVE_MEMORY_SERVICE\database\antigravity.db",
    r"c:\Users\RobsonSilva-AfixGraf\Habilidade_de_agente\01_COGNITIVE_MEMORY_SERVICE\database\evolution.db"
]

for db_path in dbs:
    if not os.path.exists(db_path):
        print(f"File not found: {db_path}")
        continue
    
    print(f"\n--- Database: {os.path.basename(db_path)} ---")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # List tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables: {[t[0] for t in tables]}")
        
        for table in [t[0] for t in tables]:
            try:
                cursor.execute(f"SELECT count(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"Table {table}: {count} records")
                
                # Show columns
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                print(f"Columns: {[c[1] for c in columns]}")
            except Exception as te:
                print(f"Error reading table {table}: {te}")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
