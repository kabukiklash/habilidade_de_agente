/**
 * Entidade Atividade - Tarefas e atividades do lead
 * @see ESPECIFICACAO_SISTEMA.md
 */
export type TipoAtividade = 'ligacao' | 'email' | 'whatsapp' | 'reuniao' | 'tarefa' | 'outro';
export type StatusAtividade = 'pendente' | 'em_andamento' | 'concluida' | 'cancelada';

export interface Atividade {
  id: string;
  leadId: string;
  tipo: TipoAtividade;
  descricao: string;
  dataAgendada?: Date;
  status: StatusAtividade;
  createdBy: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface CreateAtividadeDto {
  leadId: string;
  tipo: TipoAtividade;
  descricao: string;
  dataAgendada?: Date;
  createdBy: string;
}
