import { Router } from 'express';
import { quotesController } from './quotes.controller';

const router = Router();

// Specialized snapshot creation
router.post('/quotes/from-template', quotesController.createFromTemplate);

// Quotes Core
router.post('/quotes', quotesController.createQuote);
router.get('/quotes', quotesController.getQuotes);
router.get('/quotes/:id', quotesController.getQuote);
router.put('/quotes/:id', quotesController.updateQuote);
router.delete('/quotes/:id', quotesController.deleteQuote);

// Quote Items Editor
router.post('/quotes/:id/items', quotesController.addQuoteItem);
router.put('/quote-items/:id', quotesController.updateQuoteItem);
router.delete('/quote-items/:id', quotesController.deleteQuoteItem);

export default router;
