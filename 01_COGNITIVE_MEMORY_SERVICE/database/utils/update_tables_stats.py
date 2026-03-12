import re

filepath = 'c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/cognitive-memory-service/app/routes/tables.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'''# --- APPEND EVENTS \(Write API\) ---'''
rep = '''@router.get("/events/stats")
async def get_event_stats(db: AsyncSession = Depends(get_db)):
    """Aggregate token economy stats."""
    try:
        query = text("""
            SELECT 
                COALESCE(SUM(tokens_used), 0) as total_used,
                COALESCE(SUM(tokens_saved), 0) as total_saved
            FROM events
        """)
        result = await db.execute(query)
        row = result.fetchone()
        
        total_used = int(row.total_used) if row else 0
        total_saved = int(row.total_saved) if row else 0
        
        efficiency = 0.0
        if total_used + total_saved > 0:
            efficiency = (total_saved / (total_used + total_saved)) * 100
            
        return {
            "tokens_used": total_used,
            "tokens_saved": total_saved,
            "efficiency_percent": round(efficiency, 1)
        }
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return {"tokens_used": 0, "tokens_saved": 0, "efficiency_percent": 0.0}

# --- APPEND EVENTS (Write API) ---'''
content = re.sub(pattern, rep, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added /events/stats to tables.py successfully!")
