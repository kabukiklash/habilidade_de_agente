import re
import os

filepath = 'c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/cognitive-memory-service/app/routes/tables.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Update AppendEventRequest
pattern1 = r'''class AppendEventRequest\(BaseModel\):
    event_type: str
    actor: str
    payload: dict
    justification: Optional\[str\] = None
    correlation_id: Optional\[str\] = None
    event_id: Optional\[str\] = None # Support client-side ID'''
rep1 = '''class AppendEventRequest(BaseModel):
    event_type: str
    actor: str
    payload: dict
    justification: Optional[str] = None
    correlation_id: Optional[str] = None
    event_id: Optional[str] = None # Support client-side ID
    tokens_used: int = 0
    tokens_saved: int = 0'''
content = re.sub(pattern1, rep1, content)

# Update INSERT query
pattern2 = r'''    query_sql = """
        INSERT INTO events \(event_type, actor, payload, justification, correlation_id, event_id\)
        VALUES \(:event_type, :actor, cast\(:payload as jsonb\), :justification, :correlation_id, COALESCE\(:event_id, gen_random_uuid\(\)\)\)
        RETURNING event_id, created_at
    """'''
rep2 = '''    query_sql = """
        INSERT INTO events (event_type, actor, payload, justification, correlation_id, event_id, tokens_used, tokens_saved)
        VALUES (:event_type, :actor, cast(:payload as jsonb), :justification, :correlation_id, COALESCE(:event_id, gen_random_uuid()), :tokens_used, :tokens_saved)
        RETURNING event_id, created_at
    """'''
content = re.sub(pattern2, rep2, content)

# Update params dictionary
pattern3 = r'''    params = \{
        "event_type": request\.event_type,
        "actor": request\.actor,
        "payload": json\.dumps\(request\.payload\),
        "justification": request\.justification,
        "correlation_id": request\.correlation_id,
        "event_id": request\.event_id
    \}'''
rep3 = '''    params = {
        "event_type": request.event_type,
        "actor": request.actor,
        "payload": json.dumps(request.payload),
        "justification": request.justification,
        "correlation_id": request.correlation_id,
        "event_id": request.event_id,
        "tokens_used": request.tokens_used,
        "tokens_saved": request.tokens_saved
    }'''
content = re.sub(pattern3, rep3, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated tables.py successfully!")
