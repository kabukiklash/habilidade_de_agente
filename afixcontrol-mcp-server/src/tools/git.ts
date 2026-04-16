/**
 * Git Validation Tool
 * Chama o MCP Gateway API REST para validar git
 */

import { apiClient } from './api-client';

export async function validateGit(): Promise<any> {
  try {
    console.log('🔍 Validando git via API...');
    const result = await apiClient.request('validate_git');
    return result;
  } catch (error) {
    return {
      status: 'ERROR',
      error: String(error)
    };
  }
}
