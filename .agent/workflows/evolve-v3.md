---
description: Automatiza a evolução completa para a versão v3.0 (CMS + Kimi + Cortex)
---

Este workflow transforma um agente padrão em uma instância Antigravity v3.0.

1. Leia o Manual Mestre para entender a nova hierarquia.
// turbo
2. Execute o script de setup do ambiente.
```powershell
./Habilidade_de_agente/scripts/setup_evolution.ps1
```

3. Tente iniciar o CMS via Docker.
```powershell
cd Habilidade_de_agente/cognitive-memory-service; docker-compose up -d
```

4. Verifique a conectividade com o Kimi.
```powershell
python Habilidade_de_agente/llm_integration/test_kimi_connection.py
```

5. Carregue o `CognitiveCortex` como seu orquestrador primário.

6. Reporte ao usuário que a evolução foi concluída com sucesso.
