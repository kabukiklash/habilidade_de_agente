"""
Session Token Estimator — Evolution Sovereign System
======================================================
Estima o consumo de tokens de uma sessão de work com base em:
  - Arquivos modificados neste workspace (diff de tamanho)
  - Texto passado como argumento (contexto da conversa)
  - Tamanho de arquivos abertos (contexto de IDE)

Regras de estimativa (indústria):
  - 1 token ≈ 4 caracteres (texto inglês/código)
  - 1 token ≈ 3 caracteres (texto português/misto)
  - Gemini 1.5 / 2.0: input + output é cobrado

Uso:
  python scripts/session_token_estimator.py
  python scripts/session_token_estimator.py --log  (também salva no log_session.py)
"""

import os
import sys
import argparse
import json
from datetime import datetime
from pathlib import Path

# ─── Configurações ─────────────────────────────────────────────────────────────
WORKSPACE = Path("c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente")
CHARS_PER_TOKEN = 3.5      # Ajuste para PT-BR (misto de código + português)
LOG_FILE = WORKSPACE / "scripts" / "token_log.json"

# Arquivos que tipicamente são incluídos no contexto de uma sessão de IDE
CONTEXT_FILES = [
    "GEMINI.md",
    ".agent/agents/frontend-specialist.md",
    ".agent/agents/backend-specialist.md",
    ".cursor/rules/evolution_core.mdc",
    ".clinerules",
]

# ─── Funções ────────────────────────────────────────────────────────────────────

def count_tokens(text: str) -> int:
    """Estima o número de tokens a partir de um bloco de texto."""
    return max(1, int(len(text) / CHARS_PER_TOKEN))


def count_file_tokens(filepath: Path) -> dict:
    """Lê um arquivo e conta seus tokens estimados."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        tokens = count_tokens(content)
        return {"file": str(filepath.name), "chars": len(content), "tokens": tokens}
    except FileNotFoundError:
        return {"file": str(filepath.name), "chars": 0, "tokens": 0}


def scan_context_files() -> list:
    """Varre arquivos de contexto que a IDE provavelmente enviou para a IA."""
    results = []
    for rel_path in CONTEXT_FILES:
        full_path = WORKSPACE / rel_path
        results.append(count_file_tokens(full_path))
    return results


def scan_modified_files(hours: int = 8) -> list:
    """Encontra arquivos modificados nas últimas N horas (janela da sessão)."""
    import time
    cutoff = time.time() - (hours * 3600)
    results = []
    
    EXCLUDE = {".git", "__pycache__", "node_modules", ".venv", "venv", ".mypy_cache"}
    
    for root, dirs, files in os.walk(WORKSPACE):
        dirs[:] = [d for d in dirs if d not in EXCLUDE]
        for fname in files:
            if not fname.endswith((".py", ".md", ".json", ".ts", ".tsx", ".js", ".html", ".css")):
                continue
            fpath = Path(root) / fname
            try:
                mtime = fpath.stat().st_mtime
                if mtime >= cutoff:
                    info = count_file_tokens(fpath)
                    info["file"] = str(fpath.relative_to(WORKSPACE))
                    results.append(info)
            except Exception:
                continue
    
    return sorted(results, key=lambda x: x["tokens"], reverse=True)


def format_cost(tokens: int) -> str:
    """Estimativa de custo USD para Gemini 2.0 Flash (input ~$0.075/1M tokens)."""
    cost_usd = (tokens / 1_000_000) * 0.075
    return f"~${cost_usd:.4f} USD"


def print_report(session_name: str, hours: int):
    print("\n" + "═" * 60)
    print("🧠 EVOLUTION — SESSION TOKEN ESTIMATOR")
    print("═" * 60)
    print(f"📅 Sessão   : {session_name}")
    print(f"⏱️  Janela   : Últimas {hours} horas")
    print(f"📐 Estimativa: {CHARS_PER_TOKEN} chars/token (PT-BR misto)")
    print("═" * 60)

    # 1. Contexto fixo (GEMINI.md, cursorrules, etc.)
    ctx_files = scan_context_files()
    ctx_total = sum(f["tokens"] for f in ctx_files)
    print(f"\n📌 CONTEXTO FIXO (injetado automaticamente pela IDE)")
    for f in ctx_files:
        if f["tokens"] > 0:
            print(f"   {f['file']:<40} {f['tokens']:>8,} tokens")
    print(f"   {'SUBTOTAL contexto':<40} {ctx_total:>8,} tokens")

    # 2. Arquivos modificados na sessão
    mod_files = scan_modified_files(hours)
    mod_total = sum(f["tokens"] for f in mod_files)
    print(f"\n📝 ARQUIVOS MODIFICADOS NA SESSÃO (top 20)")
    for f in mod_files[:20]:
        print(f"   {f['file']:<40} {f['tokens']:>8,} tokens")
    if len(mod_files) > 20:
        rest = sum(f["tokens"] for f in mod_files[20:])
        print(f"   ... +{len(mod_files)-20} arquivos            {rest:>8,} tokens")
    print(f"   {'SUBTOTAL modificados':<40} {mod_total:>8,} tokens")

    # 3. Total
    grand_total = ctx_total + mod_total
    # Input + output estimate (output ~20% do input)
    estimated_output = int(grand_total * 0.2)
    billed_total = grand_total + estimated_output

    print(f"\n{'═' * 60}")
    print(f"   {'Input estimado (contexto + arquivos)':<40} {grand_total:>8,} tokens")
    print(f"   {'Output estimado (~20% do input)':<40} {estimated_output:>8,} tokens")
    print(f"   {'TOTAL FATURÁVEL ESTIMADO':<40} {billed_total:>8,} tokens")
    print(f"   {'Custo estimado (Gemini 2.0 Flash)':<40} {format_cost(billed_total):>12}")
    print("═" * 60)

    return billed_total


def save_to_log(session_name: str, tokens: int):
    """Salva o relatório no arquivo de log."""
    log = []
    if LOG_FILE.exists():
        try:
            log = json.loads(LOG_FILE.read_text(encoding="utf-8"))
        except Exception:
            log = []

    entry = {
        "timestamp": datetime.now().isoformat(),
        "session": session_name,
        "tokens_estimated": tokens,
    }
    log.append(entry)

    LOG_FILE.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n💾 Salvo em: {LOG_FILE}")


# ─── Entry Point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Session Token Estimator")
    parser.add_argument("--session", default=f"Sessao {datetime.now().strftime('%Y-%m-%d %H:%M')}", help="Nome da sessão")
    parser.add_argument("--hours", type=int, default=8, help="Janela de tempo em horas")
    parser.add_argument("--log", action="store_true", help="Salvar resultado no log JSON")
    args = parser.parse_args()

    total = print_report(args.session, args.hours)

    if args.log:
        save_to_log(args.session, total)
