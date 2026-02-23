---
description: Check GenesisCore Foundation Control Plane status and metrics
---

# /status Workflow

This workflow performs a complete diagnostic of the GenesisCore Foundation environment to ensure operational governance (NIST MANAGE/GOVERN).

## Steps

1. **Verify Backend Connection**
Check if the server is running on port 3000.

2. **Run Health Diagnostic**
// turbo
Run the specialized health check script:
```powershell
python C:\Users\RobsonSilva-AfixGraf\Habilidade_de_agente\.agent\scripts\genesis_health_check.py
```

3. **Analyze Friction**
Review the average friction reported by the script. If friction > 50, consider investigating recent `ERROR` states in `GenesisCells`.
