import re

filepath_audit = 'c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/llm_integration/audit_monitor.py'
with open(filepath_audit, 'r', encoding='utf-8') as f:
    content_audit = f.read()

pattern_audit = r'''    async def log_decision_with_intent\(
        self, 
        intent_id: str, 
        decision_payload: Dict\[str, Any\], 
        justification: str
    \):
        """
        Vincula uma decisão do Kimi a uma intenção original do usuário\.
        Adds an integrity hash for forensic verification\.
        """
        integrity_hash = self\._generate_integrity_hash\(decision_payload\)
        
        audit_payload = \{
            "intent_id": intent_id,
            "decision": decision_payload,
            "integrity_hash": integrity_hash,
            "audit_timestamp": asyncio\.get_event_loop\(\)\.time\(\)
        \}
        
        await memory_adapter\.append_event\(
            event_type="KIMI_AUDIT_LOG",
            payload=audit_payload,
            justification=f"Auditoria vinculada à intenção \{intent_id\}: \{justification\}",
            correlation_id=intent_id
        \)'''
rep_audit = '''    async def log_decision_with_intent(
        self, 
        intent_id: str, 
        decision_payload: Dict[str, Any], 
        justification: str,
        tokens_used: int = 0,
        tokens_saved: int = 0
    ):
        """
        Vincula uma decisão do Kimi a uma intenção original do usuário.
        Adds an integrity hash for forensic verification.
        """
        integrity_hash = self._generate_integrity_hash(decision_payload)
        
        audit_payload = {
            "intent_id": intent_id,
            "decision": decision_payload,
            "integrity_hash": integrity_hash,
            "audit_timestamp": asyncio.get_event_loop().time()
        }
        
        await memory_adapter.append_event(
            event_type="KIMI_AUDIT_LOG",
            payload=audit_payload,
            justification=f"Auditoria vinculada à intenção {intent_id}: {justification}",
            correlation_id=intent_id,
            tokens_used=tokens_used,
            tokens_saved=tokens_saved
        )'''
content_audit = re.sub(pattern_audit, rep_audit, content_audit)
with open(filepath_audit, 'w', encoding='utf-8') as f:
    f.write(content_audit)


filepath_cortex = 'c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/llm_integration/cognitive_cortex.py'
with open(filepath_cortex, 'r', encoding='utf-8') as f:
    content_cortex = f.read()

pattern_cortex = r'''        # 4\. Deep Thinking via Kimi
        print\(f"🚀 \[Cortex\] Routing to Kimi \(Thinking Mode\)\.\.\."\)
        try:
            solution = await kimi_client\.chat_thinking\(prompt\)'''
rep_cortex = '''        import json
        # 4. Deep Thinking via Kimi
        print(f"🚀 [Cortex] Routing to Kimi (Thinking Mode)...")
        try:
            solution, usage = await kimi_client.chat_thinking(prompt, return_usage=True)
            
            # Token Economy Math
            tokens_used = usage.get('total_tokens', 0)
            raw_tokens_estimate = len(json.dumps(raw_context)) // 4
            curated_tokens_estimate = len(json.dumps(context_pack)) // 4
            tokens_saved = max(0, raw_tokens_estimate - curated_tokens_estimate)
            print(f"💰 [Token Economy] Used: {tokens_used} | Saved by CMS: {tokens_saved}")'''
content_cortex = re.sub(pattern_cortex, rep_cortex, content_cortex)

pattern_cortex_log = r'''            # Log to Audit Monitor \(Integrity Hash\)
            await audit_monitor\.log_decision_with_intent\(
                intent_id=current_intent,
                decision_payload=decision_payload,
                justification=f"Auditoria forense para a tarefa: \{task_description\[:50\]\}"
            \)'''
rep_cortex_log = '''            # Log to Audit Monitor (Integrity Hash)
            await audit_monitor.log_decision_with_intent(
                intent_id=current_intent,
                decision_payload=decision_payload,
                justification=f"Auditoria forense para a tarefa: {task_description[:50]}",
                tokens_used=tokens_used,
                tokens_saved=tokens_saved
            )'''
content_cortex = re.sub(pattern_cortex_log, rep_cortex_log, content_cortex)

with open(filepath_cortex, 'w', encoding='utf-8') as f:
    f.write(content_cortex)

print("Updated audit_monitor.py and cognitive_cortex.py successfully!")
