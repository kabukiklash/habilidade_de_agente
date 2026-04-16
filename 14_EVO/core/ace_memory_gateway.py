import requests
import json
import os
from loop_guard_master import loop_guard

class MemoryGateway:
    """
    Gateway Soberano para escrita no CMS (TEC 01).
    Aplica governança obrigatória: Dedup, Rate Limit e Tagging.
    """
    
    def __init__(self, cms_base_url: str, api_key: str):
        self.cms_base_url = cms_base_url
        self.api_key = api_key

    def _get_headers(self):
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-ACE-API-KEY"] = self.api_key
        return headers

    def append_event(self, event_type: str, actor: str, payload: dict, justification: str):
        """
        Escrita governada de eventos.
        """
        # 1. Rate Limit Check
        if not loop_guard.check_rate_limit():
            print(f"⚠️ [Gateway] Bloqueado por Rate Limit: {event_type}")
            return False, "Rate Limit Exceeded"

        # 2. Source Tagging (Impondo soberania)
        payload["_governance"] = {
            "origin": "ace",
            "gateway_v": "2.0",
            "policy": "sovereign_governance"
        }

        # 3. Request
        try:
            endpoint = f"{self.cms_base_url}/tables/events/append"
            response = requests.post(endpoint, json={
                "event_type": event_type,
                "actor": actor,
                "payload": payload,
                "justification": justification
            }, headers=self._get_headers(), timeout=5)
            
            if response.status_code in (200, 201):
                loop_guard.register_action()
                return True, "Event appended"
            return False, f"CMS Error: {response.status_code}"
        except Exception as e:
            return False, str(e)

    def append_concept(self, name: str, description: str, node_type: str, properties: dict):
        """
        Escrita governada de conceitos (Memória de Longo Prazo).
        Aplica Deduplicação Semântica Obrigatória.
        """
        # 1. Semantic Dedup Check
        if loop_guard.is_semantic_duplicate(description):
            print(f"♻️ [Gateway] Insight descartado por duplicidade semântica: {name}")
            return False, "Semantic Duplicate Detected"

        # 2. Rate Limit Check
        if not loop_guard.check_rate_limit():
            print(f"⚠️ [Gateway] Bloqueado por Rate Limit: concept save")
            return False, "Rate Limit Exceeded"

        # 3. Source Tagging
        properties["_governance"] = {"origin": "ace", "dedup_checked": True}

        # 4. Request
        try:
            endpoint = f"{self.cms_base_url}/tables/concepts/append"
            response = requests.post(endpoint, json={
                "name": name,
                "description": description,
                "node_type": node_type,
                "properties": properties
            }, headers=self._get_headers(), timeout=5)
            
            if response.status_code in (200, 201):
                loop_guard.register_action()
                return True, "Concept appended"
            return False, f"CMS Error: {response.status_code}"
        except Exception as e:
            return False, str(e)

# O Gateway será instanciado no ace_server com a URL configurada.
