/**
 * Entidade EstagioFunil - Estágios do Kanban CRM
 * @see ESPECIFICACAO_SISTEMA.md
 */
export interface EstagioFunil {
  id: string;
  nome: string;
  ordem: number;
  cor: string;
  empresaId: string;
  probabilidadeConversao: number; // 0-100
  createdAt?: Date;
  updatedAt?: Date;
}

export interface CreateEstagioFunilDto {
  nome: string;
  ordem: number;
  cor: string;
  empresaId: string;
  probabilidadeConversao: number;
}
