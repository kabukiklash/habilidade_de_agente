import re
import os

filepath = 'C:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/antigravity_memory_backend/memory_adapter.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix append_event signature (Lines 55-63)
pattern1 = r'''    async def append_event\(
        self,
        event_type: str,
        payload: Dict\[str, Any\],
        justification: Optional\[str\] = None,
        correlation_id: Optional\[str\] = None
    \) -> Dict\[str, str\]:'''
rep1 = '''    async def append_event(
        self,
        event_type: str,
        payload: Dict[str, Any],
        justification: Optional[str] = None,
        correlation_id: Optional[str] = None,
        tokens_used: int = 0,
        tokens_saved: int = 0
    ) -> Dict[str, str]:'''
content = re.sub(pattern1, rep1, content)

# Fix appending to cms
pattern2 = r'''                result = await self\.cms_client\.append_event\(
                    event_type=event_type,
                    actor=self\.actor,
                    payload=payload,
                    justification=justification,
                    correlation_id=correlation_id
                \)'''
rep2 = '''                result = await self.cms_client.append_event(
                    event_type=event_type,
                    actor=self.actor,
                    payload=payload,
                    justification=justification,
                    correlation_id=correlation_id,
                    tokens_used=tokens_used,
                    tokens_saved=tokens_saved
                )'''
content = re.sub(pattern2, rep2, content)

# Fix fallback calls
pattern3 = r'''                if self\.sqlite_ledger:
                    return self\._append_sqlite\(event_type, payload, justification\)
                raise e
        
        if self\.sqlite_ledger:
            return self\._append_sqlite\(event_type, payload, justification\)'''
rep3 = '''                if self.sqlite_ledger:
                    return self._append_sqlite(event_type, payload, justification, correlation_id, tokens_used, tokens_saved)
                raise e
        
        if self.sqlite_ledger:
            return self._append_sqlite(event_type, payload, justification, correlation_id, tokens_used, tokens_saved)'''
content = re.sub(pattern3, rep3, content)

# Fix _append_sqlite signature
pattern4 = r'''    def _append_sqlite\(
        self,
        event_type: str,
        payload: Dict\[str, Any\],
        justification: Optional\[str\] = None
    \) -> Dict\[str, str\]:'''
rep4 = '''    def _append_sqlite(
        self,
        event_type: str,
        payload: Dict[str, Any],
        justification: Optional[str] = None,
        correlation_id: Optional[str] = None,
        tokens_used: int = 0,
        tokens_saved: int = 0
    ) -> Dict[str, str]:'''
content = re.sub(pattern4, rep4, content)

# Fix record_event body
pattern5 = r'''        import json
        event_id = self\.sqlite_ledger\.append\(\{
            "event_type": event_type,
            "actor": self\.actor,
            "payload": payload,
            "justification": justification,
            "timestamp": datetime\.utcnow\(\)\.isoformat\(\)
        \}\)'''
rep5 = '''        import json
        event_id = self.sqlite_ledger.record_event(
            event_type=event_type,
            payload=payload,
            justification=justification or "Direct SQLite Append",
            correlation_id=correlation_id,
            actor_id=self.actor,
            tokens_used=tokens_used,
            tokens_saved=tokens_saved
        )'''
content = re.sub(pattern5, rep5, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated memory_adapter.py successfully!")
