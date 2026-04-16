/**
 * Database Validation Tool
 * Chama o MCP Gateway API REST para validar banco de dados
 */

import { apiClient } from './api-client';

export async function validateDatabase(): Promise<any> {
  try {
    console.log('🔍 Validando banco de dados via API...');
    const result = await apiClient.request('validate_database');
    return result;
  } catch (error) {
    return {
      status: 'ERROR',
      error: String(error)
    };
  }
}
