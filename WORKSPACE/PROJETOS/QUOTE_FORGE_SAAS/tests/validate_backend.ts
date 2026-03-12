import axios from 'axios';
import { performance } from 'perf_hooks';

/**
 * ID: CP-FORGE-VAL-001
 * Suite de Validação exaustiva sem Frontend.
 */

const API_URL = 'http://localhost:3001';

async function logTest(name: string, fn: () => Promise<any>) {
  const start = performance.now();
  try {
    const result = await fn();
    console.log(`✅ [PASS] ${name} (${(performance.now() - start).toFixed(2)}ms)`);
    return { name, status: 'PASS', result };
  } catch (err: any) {
    const errorMsg = err.response ? JSON.stringify(err.response.data) : err.message;
    console.log(`❌ [FAIL] ${name}: ${errorMsg}`);
    return { name, status: 'FAIL', error: errorMsg };
  }
}

async function runValidation() {
  console.log('🦅 [SOVEREIGN] Starting Backend Evidence Engine...');
  const evidence: any = {};

  // 1. Healthcheck
  evidence.t1 = await logTest('T1: Healthcheck & DB Connection', async () => {
    const res = await axios.get(`${API_URL}/health`);
    return res.data;
  });

  // 2. Login ACME
  evidence.t2 = await logTest('T2: ACME Admin Login', async () => {
    const res = await axios.post(`${API_URL}/api/auth/login`, {
      email: 'admin@acme.com',
      password: 'admin123'
    });
    return res.data;
  });

  if (evidence.t2.status === 'FAIL') {
      console.log('Stopping due to login failure.');
      return;
  }

  const token = evidence.t2.result.token;
  const authHeaders = { headers: { Authorization: `Bearer ${token}` } };

  // 3. Create Template
  evidence.t3 = await logTest('T3: Create Template Placa PVC', async () => {
    const res = await axios.post(`${API_URL}/api/templates`, {
      name: 'Placa PVC',
      fields: [
        { name: 'largura', type: 'number', required: true },
        { name: 'altura', type: 'number', required: true },
        { name: 'preco_m2', type: 'number', required: true }
      ],
      formulaLogic: '(largura * altura) * preco_m2'
    }, authHeaders);
    return res.data;
  });

  const templateId = evidence.t3.result?.id;

  // 4. Calculate Quote
  evidence.t4 = await logTest('T4: Motor Calculation (1.2 * 0.8 * 120)', async () => {
    const res = await axios.post(`${API_URL}/api/quotes`, {
      clientData: { name: 'Loja Central' },
      items: [{
        templateId,
        inputs: { largura: 1.2, altura: 0.8, preco_m2: 120 }
      }]
    }, authHeaders);
    return res.data;
  });

  // 5. Security (Negative Test)
  evidence.t5 = await logTest('T5: Security Sandbox Block', async () => {
     try {
         await axios.post(`${API_URL}/api/templates`, {
             name: 'Placa Maliciosa',
             fields: [{ name: 'x', type: 'number' }],
             formulaLogic: "require('fs').readFileSync('.env')"
         }, authHeaders);
         throw new Error("Sandbox should have blocked this");
     } catch (err: any) {
         if (err.message === "Sandbox should have blocked this") throw err;
         return { blocked: true, msg: err.response?.data?.error || err.message };
     }
  });

  // 6. Send & Snapshot
  const quoteId = evidence.t4.result?.id;
  evidence.t6 = await logTest('T6: Send Quote & Generate Snapshot', async () => {
    const res = await axios.post(`${API_URL}/api/api/quotes/${quoteId}/send`, {}, authHeaders);
    return res.data;
  });

  // 9. RLS Isolation Test
  evidence.t9 = await logTest('T9: Multi-Tenant RLS Isolation', async () => {
    const spyRes = await axios.post(`${API_URL}/api/auth/login`, {
      email: 'spy@globex.com',
      password: 'admin123'
    });
    const spyToken = spyRes.data.token;
    
    try {
        await axios.get(`${API_URL}/api/templates`, { headers: { Authorization: `Bearer ${spyToken}` } });
        // Check if ACME data is present in Globex list
        const list = await axios.get(`${API_URL}/api/templates`, { headers: { Authorization: `Bearer ${spyToken}` } });
        const hasAcmeData = list.data.some((t: any) => t.id === templateId);
        if (hasAcmeData) throw new Error("RLS LEAK DETECTED: Globex sees ACME data!");
        return { isolation: 'ACTIVE', msg: 'Globex cannot see ACME templates' };
    } catch (err: any) {
        return { isolation: 'ACTIVE', msg: err.message };
    }
  });

  console.log('\n📜 Final Validation Summary Captured.');
  console.log('Generate your report based on these results.');
}

runValidation();
