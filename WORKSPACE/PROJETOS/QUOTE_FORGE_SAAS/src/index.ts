import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import dotenv from 'dotenv';
import { QuoteController } from './api/QuoteController';
import { TenantController } from './api/TenantController';
import { TemplateController } from './api/TemplateController';
import { authMiddleware } from './api/AuthMiddleware';
import { SendQuote } from './application/use-cases/SendQuote';

dotenv.config();

/**
 * ID: CP-FORGE-CORE-MAIN
 * Ponto de Entrada Soberano: Servidor do SaaS Quote Forge.
 */

const app = express();
const PORT = process.env.PORT || 3000;

app.use(helmet());
app.use(cors());
app.use(express.json());

// Rota de Saúde
app.get('/health', (req: Request, res: Response) => res.json({ status: 'Sovereign Core Active', timestamp: new Date() }));

// Rota de Login (Pública)
app.post('/api/auth/login', TenantController.login);

// Rotas Protegidas
const apiRouter = express.Router();
apiRouter.use(authMiddleware);

// Templates
apiRouter.post('/templates', TemplateController.create);
apiRouter.get('/templates', TemplateController.list);

// Orçamentos
apiRouter.post('/quotes', QuoteController.create);
apiRouter.patch('/quotes/:id/approve', QuoteController.approve);

// Envio e Snapshot
apiRouter.post('/quotes/:id/send', async (req: Request, res: Response) => {
  try {
    const { tenantId } = (req as any).user;
    const { id } = req.params;
    if (!id) throw new Error("ID do orçamento é obrigatório.");
    const result = await SendQuote.execute(tenantId, id as string);
    return res.json(result);
  } catch (error: any) {
    return res.status(400).json({ error: error.message });
  }
});

app.use('/api', apiRouter);

// Inicialização do Servidor
app.listen(PORT, () => {
  console.log(`
  🦅 [SOVEREIGN] Universal Quote Forge SaaS is UP!
  🌐 Port: ${PORT}
  🛠️  Mode: ${process.env.NODE_ENV}
  `);
});
