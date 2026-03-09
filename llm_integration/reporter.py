def print_token_economy_report(tokens_used: int, tokens_saved: int, execution_time_ms: int = None):
    """
    Prints a beautiful, terminal-formatted Token Economy Report for Investors.
    """
    efficiency = 0.0
    if tokens_used + tokens_saved > 0:
        efficiency = (tokens_saved / (tokens_used + tokens_saved)) * 100

    print("\n" + "="*50)
    print(" 📈 ANTIGRAVITY TOKEN ECONOMY REPORT")
    print("="*50)
    print(f" 🔹 Tokens Used   : {tokens_used:,}")
    print(f" 🟩 Tokens Saved  : {tokens_saved:,} (by CMS Curation)")
    print(f" ⚡ Efficiency    : {efficiency:.1f}%")
    if execution_time_ms is not None:
        print(f" ⏱️  Execution Time: {execution_time_ms} ms")
    print("="*50 + "\n")
