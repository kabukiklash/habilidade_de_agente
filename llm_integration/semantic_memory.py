import sqlite3
import json
import numpy as np
from typing import List, Dict, Any, Optional

class SemanticMemory:
    """
    Antigravity Semantic Memory Layer.
    Uses SQLite for vector storage and manual Cosine Similarity for portability.
    """
    def __init__(self, db_path: str = "C:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/antigravity.db"):
        self.db_path = db_path
        self._initialize_semantic_db()

    def _initialize_semantic_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS semantic_index (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT UNIQUE,
                    content_text TEXT,
                    embedding BLOB,  -- Serialized numpy array
                    metadata JSONB,
                    FOREIGN KEY(event_id) REFERENCES audit_ledger(event_id)
                )
            """)
            conn.commit()

    def _cosine_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def add_memory(self, event_id: str, content: str, embedding: List[float], metadata: Dict[str, Any] = None):
        emb_blob = np.array(embedding, dtype=np.float32).tobytes()
        meta_str = json.dumps(metadata) if metadata else "{}"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO semantic_index (event_id, content_text, embedding, metadata)
                VALUES (?, ?, ?, ?)
            """, (event_id, content, emb_blob, meta_str))
            conn.commit()

    def search(self, query_embedding: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        q_emb = np.array(query_embedding, dtype=np.float32)
        results = []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT event_id, content_text, embedding, metadata FROM semantic_index")
            rows = cursor.fetchall()
            
            for row in rows:
                event_id, content, emb_blob, meta = row
                db_emb = np.frombuffer(emb_blob, dtype=np.float32)
                score = self._cosine_similarity(q_emb, db_emb)
                results.append({
                    "event_id": event_id,
                    "content": content,
                    "score": float(score),
                    "metadata": json.loads(meta)
                })
        
        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

if __name__ == "__main__":
    # Mock Test for portability confirmation
    print("[*] Initializing Semantic Memory Test...")
    memory = SemanticMemory()
    
    # Mock Embeddings (Size 1536 like Gemini/OpenAI)
    mock_emb_1 = np.random.rand(1536).tolist()
    mock_emb_2 = np.random.rand(1536).tolist()
    
    memory.add_memory("test-event-1", "Security protocol alpha", mock_emb_1, {"tag": "security"})
    memory.add_memory("test-event-2", "UI Glassmorphism guidelines", mock_emb_2, {"tag": "design"})
    
    # Search with something close to mock_emb_1
    search_results = memory.search(mock_emb_1)
    print(f"Top Result Score: {search_results[0]['score']}")
    if search_results[0]['event_id'] == "test-event-1":
        print("✅ Semantic Search Logic Validated.")
