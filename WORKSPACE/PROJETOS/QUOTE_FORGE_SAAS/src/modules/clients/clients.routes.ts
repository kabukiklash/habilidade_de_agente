import { Router } from 'express';
import { clientsController } from './clients.controller';

const router = Router();

router.post('/clients', clientsController.createClient);
router.get('/clients', clientsController.getClients);
router.get('/clients/:id', clientsController.getClient);
router.put('/clients/:id', clientsController.updateClient);
router.delete('/clients/:id', clientsController.deleteClient);

export default router;
