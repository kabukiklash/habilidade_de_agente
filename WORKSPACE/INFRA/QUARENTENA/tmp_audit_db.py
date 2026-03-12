import sqlite3
import json
import os

db_path = 'c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/antigravity.db'

def audit():
    if not os.path.exists(db_path):
        return {"error": f"Database not found at {db_path}"}
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    stats = {}
    
    # 1. Total Events (Ledger Density)
    cursor.execute("SELECT COUNT(*) FROM audit_ledger")
    stats['total_events'] = cursor.fetchone()[0]
    
    # 2. Token Economy (ROI)
    cursor.execute("SELECT SUM(tokens_saved) FROM audit_ledger")
    stats['total_tokens_saved'] = cursor.fetchone()[0] or 0
    
    # 3. Memory Nodes (Knowledge Graph)
    cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='semantic_index'")
    if cursor.fetchone():
        cursor.execute("SELECT COUNT(*) FROM semantic_index")
        stats['memory_nodes'] = cursor.fetchone()[0]
    else:
        stats['memory_nodes'] = 0
        
    conn.close()
    return stats

if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
