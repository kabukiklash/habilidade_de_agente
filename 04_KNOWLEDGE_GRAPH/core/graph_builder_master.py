import re
import json
import os
import sys
from typing import List, Dict, Any, Set

# Sovereign Path Orchestration
base_dir = "c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente"
tech_01_client = os.path.join(base_dir, "01_COGNITIVE_MEMORY_SERVICE", "client")
tech_07_core = os.path.join(base_dir, "07_KIMI_MEMORY_BRIDGE", "core")
tech_02_cortex = os.path.join(base_dir, "02_COGNITIVE_CORTEX", "core")

for p in [tech_01_client, tech_07_core, tech_02_cortex]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Fallback Logger logic
try:
    from .logger import logger
except ImportError:
    class DummyLogger:
        def info(self, m): print(f"[INFO] {m}")
        def error(self, m): print(f"[ERROR] {m}")
        def warning(self, m): print(f"[WARN] {m}")
    logger = DummyLogger()

from cms_client_master import cms_client

class GraphBuilder:
    """
    Motor de Extração de Grafo do Antigravity.
    Transforma texto técnico em uma rede de Conceitos e Links.
    """
    
    def __init__(self):
        # Stopwords técnicas para filtrar conceitos irrelevantes
        self.technical_stopwords = {"the", "and", "this", "that", "with", "from", "into", "using"}
        # Padrões para identificar entidades técnicas (Fallback)
        self.patterns = {
            "function": r"(?:def\s+|função\s+)([a-zA-Z_][a-zA-Z0-9_]*)",
            "class": r"(?:class\s+|classe\s+)([a-zA-Z_][a-zA-Z0-9_]*)",
            "file": r"([a-zA-Z0-9_/.-]+\.(?:py|js|ts|css|html|md))",
            "component": r"@([a-zA-Z_][a-zA-Z0-9_]*)",
            "concept": r"\[\[(.*?)\]\]"
        }
        
        # Integração com o Cérebro Central
        from cognitive_cortex_master import cognitive_cortex
        self.cortex = cognitive_cortex

    async def process_solution(self, text: str, correlation_id: str, mode: str = "semantic") -> Dict[str, Any]:
        """
        Analisa o texto da solução e extrai o grafo de conhecimento.
        Persiste no CMS.
        """
        if mode == "semantic":
            # Extração avançada via LLM (Semana 2 Roadmap)
            nodes, links = await self._extract_semantic_graph(text, correlation_id)
        else:
            # Fallback para Regex (Legado)
            nodes = self._extract_nodes(text)
            links = self._generate_links(nodes)
        
        if nodes or links:
            logger.info(f"🕸️ [GraphBuilder] Modo: {mode}. Extraídos {len(nodes)} nós e {len(links)} links.")
            await self._persist_to_cms(nodes, links, correlation_id)
        
        return {"nodes_count": len(nodes), "links_count": len(links), "mode": mode}

    async def _extract_semantic_graph(self, text: str, correlation_id: str) -> tuple:
        """Usa o Cognitive Cortex para extrair triplas semânticas (Entidade -> Relação -> Entidade)."""
        prompt = f"""
        Extraia entidades técnicas e suas relações do texto abaixo. 
        Retorne APENAS um objeto JSON válido no formato:
        {{
            "nodes": [ {{"name": "nome", "type": "function|class|module|db|env"}} ],
            "links": [ {{"source": "nome_origem", "target": "nome_destino", "type": "depends_on|calls|modifies|reads"}} ]
        }}
        
        TEXTO: {text}
        """
        try:
            # Chama o Cortex (usando o provedor padrão configurado)
            response_text = await self.cortex.solve_task(prompt, intent_id=correlation_id)
            
            # Tenta limpar e parsear o JSON retornado pelo LLM
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            if start_idx != -1 and end_idx != -1:
                data = json.loads(response_text[start_idx:end_idx])
                return data.get("nodes", []), data.get("links", [])
            
            return [], []
        except Exception as e:
            logger.error(f"❌ [GraphBuilder] Erro na extração semântica: {e}")
            return [], []

    def _extract_nodes(self, text: str) -> List[Dict[str, str]]:
        nodes = []
        seen = set()

        for node_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                name = match.group(1) if node_type != "file" else match.group(0)
                # Limpeza de espaços apenas, mantém case para classes/funções
                name = name.strip()
                
                name_lower = name.lower()
                if name and name_lower not in self.technical_stopwords and name_lower not in seen:
                    nodes.append({"name": name, "type": node_type})
                    seen.add(name_lower)
        
        return nodes

    def _generate_links(self, nodes: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Gera links automáticos baseados na co-ocorrência no mesmo bloco de texto (simplificado)"""
        links = []
        if len(nodes) < 2:
            return links
            
        # Cria um link central entre todos os nós extraídos na mesma tarefa
        # Em uma versão avançada, isso usaria análise semântica de proximidade
        main_node = nodes[0]["name"]
        for i in range(1, len(nodes)):
            links.append({
                "source": main_node,
                "target": nodes[i]["name"],
                "type": "related_to"
            })
        return links

    async def _persist_to_cms(self, nodes: List[Dict], links: List[Dict], correlation_id: str):
        """Salva o grafo no CMS através do memory_adapter"""
        # Nota: Usamos append_event para que o CMS possa processar as entidades de forma assíncrona/segura
        # No futuro, o CMS pode ter um endpoint direto /graph/upsert
        try:
            from memory_adapter_master import memory_adapter
            await memory_adapter.append_event(
                event_type="GRAPH_BATCH_UPDATE",
                payload={"nodes": nodes, "links": links},
                justification="Extração automática de conceitos do Knowledge Graph.",
                correlation_id=correlation_id
            )
        except Exception as e:
            logger.error(f"❌ [GraphBuilder] Falha ao persistir no CMS: {e}")

# Global Instance
graph_builder = GraphBuilder()
