/**
 * Encoding Validation Tool
 * Chama o MCP Gateway API REST para validar encoding
 */

import { apiClient } from './api-client';

export async function validateEncoding(): Promise<any> {
  try {
    console.log('🔍 Validando encoding via API...');
    const result = await apiClient.request('validate_encoding');
    return result;
  } catch (error) {
    return {
      status: 'ERROR',
      error: String(error)
    };
  }
}
