/**
 * ID: CP-FORGE-DOM-001
 * Entidades de Domínio: Regras puras do motor de orçamentos.
 */

export interface TenantDomain {
  id: string;
  name: string;
  config: Record<string, any>;
  status: 'active' | 'suspended';
}

export interface ProductTemplateDomain {
  id: string;
  tenantId: string;
  name: string;
  fields: Array<{ name: string, type: 'number' | 'string' }>;
  formulaLogic: string;
}

export interface QuoteDomain {
  id: string;
  tenantId: string;
  userId: string;
  clientData: Record<string, any>;
  totalPrice: number;
  status: 'draft' | 'sent' | 'approved' | 'rejected';
  version: number;
}
