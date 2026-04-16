/**
 * AfixControl MCP Server
 * Fornece tools para validação de database, encoding, git e testes
 */

import { config, validateConfig } from './config/index';

// Importar todas as tools (serão criadas)
import { validateDatabase } from './tools/database';
import { validateEncoding } from './tools/encoding';
import { validateGit } from './tools/git';
import { executePHPTests } from './tools/tests';

interface Tool {
  name: string;
  description: string;
  inputSchema: object;
  execute: (args: any) => Promise<any>;
}

const tools: Tool[] = [
  {
    name: 'validate_database',
    description: 'Valida conexão MySQL e índices do AfixControl',
    inputSchema: {},
    execute: validateDatabase
  },
  {
    name: 'validate_encoding',
    description: 'Valida encoding UTF-8 dos arquivos principais',
    inputSchema: {},
    execute: validateEncoding
  },
  {
    name: 'validate_git',
    description: 'Valida estado do git e cria backup tag',
    inputSchema: {},
    execute: validateGit
  },
  {
    name: 'execute_tests',
    description: 'Executa testes PHP dos filtros',
    inputSchema: {},
    execute: executePHPTests
  }
];

/**
 * Simular MCP Protocol (stdio-based)
 * Em produção, isso seria via stdin/stdout
 */
async function main() {
  try {
    validateConfig();
    console.log('🚀 AfixControl MCP Server iniciado');
    console.log(`📊 Tools disponíveis: ${tools.length}`);
    tools.forEach(t => console.log(`   - ${t.name}`));

    // Para desenvolvimento: executar validate_database como teste
    if (process.env.AUTO_TEST === 'true') {
      console.log('\n🧪 Executando AUTO_TEST...');
      const result = await validateDatabase();
      console.log('✅ Resultado:', JSON.stringify(result, null, 2));
    }
  } catch (error) {
    console.error('❌ Erro ao inicializar:', error);
    process.exit(1);
  }
}

main();
