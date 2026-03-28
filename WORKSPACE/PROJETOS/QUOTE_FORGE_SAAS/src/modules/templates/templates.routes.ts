import { Router } from 'express';
import { templatesController } from './templates.controller';

const router = Router();

// Templates
router.post('/templates', templatesController.createTemplate);
router.get('/templates', templatesController.getTemplates);
router.get('/templates/:id', templatesController.getTemplate);
router.put('/templates/:id', templatesController.updateTemplate);
router.delete('/templates/:id', templatesController.deleteTemplate);

// Template Items directly
router.post('/templates/:id/items', templatesController.addTemplateItem);
router.delete('/template-items/:id', templatesController.deleteTemplateItem);

export default router;
