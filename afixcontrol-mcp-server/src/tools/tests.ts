/**
 * Tests Execution Tool
 * Chama o MCP Gateway API REST para executar testes
 */

import { apiClient } from './api-client';

export async function executePHPTests(): Promise<any> {
  try {
    console.log('🔍 Executando testes via API...');
    const result = await apiClient.request('execute_tests');
    return result;
  } catch (error) {
    return {
      status: 'ERROR',
      error: String(error)
    };
  }
}
