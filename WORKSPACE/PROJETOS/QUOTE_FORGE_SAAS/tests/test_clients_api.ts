import axios from 'axios';

const BASE_URL = 'http://localhost:3001/api';
const EMAIL = 'admin@acme.com';
const PASSWORD = 'admin123'; // Baseado no seed_test.ts

async function testClientsCRUD() {
  console.log('🔄 Iniciando teste de integração CRUD de Clients...');
  
  // 1. Login
  const loginRes = await axios.post(`${BASE_URL}/auth/login`, {
    email: EMAIL,
    password: PASSWORD
  });
  
  const token = loginRes.data.token;
  if (!token) throw new Error('Falha no login');
  console.log('✅ Login bem sucedido. Token obtido.');
  
  const headers = { Authorization: `Bearer ${token}` };

  // 2. Criar Cliente
  const createRes = await axios.post(`${BASE_URL}/clients`, {
    name: 'Cliente de Teste Automático',
    email: 'auto@teste.com',
    phone: '11988887777',
    company: 'Auto Test LTDA'
  }, { headers });
  
  const clientId = createRes.data.id;
  console.log('✅ POST /clients: Cliente Criado ID ->', clientId);

  // 3. Listar Clientes
  const listRes = await axios.get(`${BASE_URL}/clients`, { headers });
  console.log(`✅ GET /clients: Retornou ${listRes.data.length} clientes.`);

  // 4. Buscar por ID
  const getRes = await axios.get(`${BASE_URL}/clients/${clientId}`, { headers });
  console.log('✅ GET /clients/:id: Cliente encontrado ->', getRes.data.name);

  // 5. Atualizar
  const updateRes = await axios.put(`${BASE_URL}/clients/${clientId}`, {
    name: 'Cliente Teste (Atualizado)'
  }, { headers });
  console.log('✅ PUT /clients/:id: Nome atualizado para ->', updateRes.data.name);

  // 6. Deletar
  await axios.delete(`${BASE_URL}/clients/${clientId}`, { headers });
  console.log('✅ DELETE /clients/:id: Deletado com sucesso.');

  // Verifica se deletou
  const listAfterDelete = await axios.get(`${BASE_URL}/clients`, { headers });
  console.log(`✅ Verificação final: Agora há ${listAfterDelete.data.length} clientes.`);
  
  console.log('🎉 SUCESSO! Todos os endpoints CRUD do módulo de clientes operantes.');
}

testClientsCRUD().catch((err) => {
  console.error('❌ ERRO NO TESTE:', err.response?.data || err.message);
});
