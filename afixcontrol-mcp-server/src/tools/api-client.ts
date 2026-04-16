/**
 * API Client - Conecta ao MCP Gateway PHP
 * Abstração para fazer requisições HTTP à API REST local
 */

export class APIClient {
  private baseUrl: string;

  constructor(baseUrl: string = 'http://localhost:8051') {
    this.baseUrl = baseUrl;
  }

  async request(action: string): Promise<any> {
    try {
      const url = `${this.baseUrl}/api/mcp-gateway.php?action=${action}`;
      console.log(`📡 Chamando: ${url}`);

      // Usar fetch nativo do Node.js 18+
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error(`❌ Erro ao chamar API:`, error);
      return {
        status: 'ERROR',
        error: String(error)
      };
    }
  }
}

// Exportar instância padrão
export const apiClient = new APIClient();
