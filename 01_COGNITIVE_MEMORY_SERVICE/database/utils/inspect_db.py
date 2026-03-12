import sqlite3
import json

db_path = 'c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/core/database/antigravity.db'

def list_tables():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    
    schema = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        schema[table] = [col[1] for col in cursor.fetchall()]
        
    conn.close()
    return schema

if __name__ == "__main__":
    print(json.dumps(list_tables(), indent=2))
