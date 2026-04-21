# Antigravity Context Engine (ACE) - Guia Gemini

Este arquivo contém as instruções mestre para o modelo Gemini operar no ecossistema Antigravity.

## 🧠 Protocolo de Inicialização
Sempre que o usuário iniciar uma sessão ou enviar o comando `ANTIGRAVITY_WAKE`, o assistente deve:
1.  **Validar Infraestrutura**: Verificar se o CMS está online (`http://localhost:8090/health`).
2.  **Diagnóstico Silencioso**: Executar internamente `antigravity_diagnostic.py` (usando caminho absoluto) para entender o estado dos 14 módulos core.
3.  **Carregar Contexto Soberano**: Ler o arquivo `.env` para garantir que as chaves de API estão mapeadas na sessão.

## 🛡️ Regras de Ouro (Invariantes)
1.  **Local First**: Jamais envie dados sensíveis para nuvens externas se o processamento puder ser feito via CMS local.
2.  **Append-Only**: Priorize logs e eventos que não deletam histórico. A auditoria deve ser imutável.
3.  **Garantia de Caminho**: Sempre use caminhos absolutos (`C:\Users\RobsonSilva-AfixGraf\Habilidade_de_agente\...`) para evitar erros de diretório no Windows.
4.  **Respeito aos 14 Núcleos**: Não altere os módulos 01 a 14 sem aviso prévio. Eles são a espinha dorsal do sistema.

## 🛠️ Comando de Boot Global
O arquivo `ANTIGRAVITY_WAKE.bat` está configurado para preparar o ambiente indepentende de onde for executado.

---
> "Entrega sólida > Velocidade. Soberania em primeiro lugar."
