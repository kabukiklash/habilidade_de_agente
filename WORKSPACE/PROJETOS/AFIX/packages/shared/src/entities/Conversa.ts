/**
 * Entidade Conversa - Contexto conversacional WhatsApp
 * @see ESPECIFICACAO_SISTEMA.md - Módulo Atendimento Automatizado
 */
export type TipoMensagem = 'texto' | 'imagem' | 'audio' | 'documento' | 'video';
export type OrigemMensagem = 'cliente' | 'atendente' | 'bot';

export interface Mensagem {
  id: string;
  conversaId: string;
  conteudo: string;
  tipo: TipoMensagem;
  origem: OrigemMensagem;
  whatsappMessageId?: string;
  timestamp: Date;
  metadata?: Record<string, unknown>;
}

export interface Conversa {
  id: string;
  leadId: string;
  empresaId: string;
  numeroWhatsapp: string;
  status: 'ativa' | 'encerrada' | 'aguardando';
  atendenteId?: string;
  afixScore?: number; // Predição IA 0-100
  createdAt: Date;
  updatedAt: Date;
  ultimaMensagemAt?: Date;
}
