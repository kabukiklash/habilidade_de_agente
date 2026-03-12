/**
 * Entidade Lead - CRM e Funil de Vendas
 * @see ESPECIFICACAO_SISTEMA.md
 */
export interface Lead {
  id: string;
  nome: string;
  telefone: string;
  email?: string;
  origem: string;
  tags: string[];
  score: number; // 0-100 (Afix Score)
  estagioFunilId: string;
  valorPotencial?: number;
  responsavelId?: string;
  empresaId: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface CreateLeadDto {
  nome: string;
  telefone: string;
  email?: string;
  origem: string;
  tags?: string[];
  estagioFunilId: string;
  valorPotencial?: number;
  responsavelId?: string;
  empresaId: string;
}

export interface UpdateLeadDto {
  nome?: string;
  telefone?: string;
  email?: string;
  tags?: string[];
  score?: number;
  estagioFunilId?: string;
  valorPotencial?: number;
  responsavelId?: string;
}
