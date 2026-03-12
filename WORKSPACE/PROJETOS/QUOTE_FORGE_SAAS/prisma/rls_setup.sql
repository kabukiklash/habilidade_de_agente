-- 🛡️ PROTOCOLO DE SEGURANÇA: ROW LEVEL SECURITY (RLS)
-- Este script configura o isolamento físico entre Tenants no PostgreSQL.

-- 1. Habilitar RLS nas tabelas críticas
ALTER TABLE tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE quotes ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- 2. Criar Política de Isolamento para Tenants
-- A política verifica a variável de sessão 'app.tenant_id'
CREATE POLICY tenant_isolation_policy ON product_templates
USING ("tenantId" = current_setting('app.tenant_id'));

CREATE POLICY tenant_isolation_policy ON quotes
USING ("tenantId" = current_setting('app.tenant_id'));

CREATE POLICY tenant_isolation_policy ON audit_logs
USING ("tenantId" = current_setting('app.tenant_id'));

-- 3. Função para mudar contexto de Tenant (usada pelo backend)
CREATE OR REPLACE FUNCTION set_tenant(t_id uuid) RETURNS void AS $$
BEGIN
    PERFORM set_config('app.tenant_id', t_id::text, false);
END;
$$ LANGUAGE plpgsql;
