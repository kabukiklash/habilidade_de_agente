import re

filepath = 'c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/cognitive-memory-service/app/routes/tables.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'''# --- APPEND EVENTS \(Write API\) ---'''
rep = '''@router.get("/events/history")
async def get_event_history(limit: int = 50, db: AsyncSession = Depends(get_db)):
    """Fetch the latest token economy events for the ledger audit."""
    try:
        query = text("""
            SELECT 
                id, 
                event_type, 
                justification,
                correlation_id,
                tokens_used, 
                tokens_saved,
                created_at,
                (tokens_used + tokens_saved) as raw_context_tokens
            FROM events
            ORDER BY created_at DESC
            LIMIT :limit
        """)
        result = await db.execute(query, {"limit": limit})
        
        import hashlib
        
        history = []
        for row in result:
            # Reconstruct an integrity hash for display purposes like audit_monitor
            hash_target = f"{row.correlation_id}_{row.tokens_used}_{row.tokens_saved}_{row.created_at}"
            integrity_hash = hashlib.sha256(hash_target.encode()).hexdigest()
            
            history.append({
                "id": str(row.id),
                "event_type": row.event_type,
                "justification": row.justification,
                "intent_id": row.correlation_id,
                "tokens_used": row.tokens_used if row.tokens_used else 0,
                "tokens_saved": row.tokens_saved if row.tokens_saved else 0,
                "raw_tokens": row.raw_context_tokens if row.raw_context_tokens else 0,
                "timestamp": row.created_at.isoformat(),
                "integrity_hash": integrity_hash
            })
            
        return {"data": history}
    except Exception as e:
        print(f"Error fetching history: {e}")
        return {"data": []}

# --- APPEND EVENTS (Write API) ---'''

if "/events/history" not in content:
    content = re.sub(pattern, rep, content)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added /events/history successfully")
else:
    print("History endpoint already exists.")
