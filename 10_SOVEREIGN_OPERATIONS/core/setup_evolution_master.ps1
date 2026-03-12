# Setup Evolution v3.0 - Antigravity
Write-Host "📡 Iniciando Setup de Evolução Antigravity v3.0..." -ForegroundColor Cyan

# 1. Dependências Python
Write-Host "📦 Instalando dependências Python..."
pip install httpx sqlalchemy pydantic python-dotenv asyncpg --quiet

# 2. Verificação Docker
Write-Host "🐳 Verificando Docker para o CMS..."
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "✅ Docker encontrado."
} else {
    Write-Warning "⚠️ Docker não encontrado. O CMS não poderá ser iniciado automaticamente."
}

# 3. Verificação de Chaves
Write-Host "🔑 Verificando credenciais..."
if (Test-Path "Habilidade_de_agente/.env.moonshot") {
    Write-Host "✅ Chave Moonshot encontrada."
} else {
    Write-Warning "❌ .env.moonshot ausente! A integração com Kimi k2.5 falhará."
}

Write-Host "🚀 Setup Completo. Sistema pronto para evolução v3.0!" -ForegroundColor Green
