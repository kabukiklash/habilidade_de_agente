/**
 * Configuração do MCP Server para AfixControl
 * Carrega credenciais do ambiente ou padrões
 */

export const config = {
  mysql: {
    host: process.env.AFIXCONTROL_DB_HOST || 'localhost',
    port: parseInt(process.env.AFIXCONTROL_DB_PORT || '3306'),
    user: process.env.AFIXCONTROL_DB_USER || 'root',
    password: process.env.AFIXCONTROL_DB_PASSWORD || '',
    database: process.env.AFIXCONTROL_DB_NAME || 'afixcontrol'
  },

  paths: {
    repo: process.env.AFIXCONTROL_REPO_PATH ||
      'C:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/WORKSPACE/PROJETOS/AfixcontrolAfixgraf',
    filesEncoding: [
      '_propostas/propostas.php',
      '_propostas/proposta.php',
      'classes/propostas.php',
      'ajax/propostas.php',
      'assets/pages/propostas.js'
    ]
  },

  validation: {
    whitelist_estados: ['aprovada', 'em_negociacao', 'recusada', 'pendente'],
    regex_mes_ano: /^\d{4}-\d{2}$/,
    expected_index: 'idx_proposta_estado'
  }
};

export function validateConfig(): void {
  if (!config.mysql.host) {
    throw new Error('AFIXCONTROL_DB_HOST não está configurado');
  }
  if (!config.paths.repo) {
    throw new Error('AFIXCONTROL_REPO_PATH não está configurado');
  }
  console.log('✅ Config validada');
}
