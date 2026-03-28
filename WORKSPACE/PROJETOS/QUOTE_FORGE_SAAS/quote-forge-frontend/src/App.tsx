import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Login } from './pages/Login';
import { Dashboard } from './pages/Dashboard';
import { AdminLayout } from './components/layout/AdminLayout';
import { ProtectedRoute } from './components/ProtectedRoute';
import { ClientsPage } from './pages/ClientsPage';
import { TemplatesPage } from './pages/TemplatesPage';
import { QuotesPage } from './pages/QuotesPage';
import { QuoteBuilderPage } from './pages/QuoteBuilderPage';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          
          <Route element={<ProtectedRoute />}>
            <Route element={<AdminLayout />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/templates" element={<TemplatesPage />} />
              <Route path="/quotes" element={<QuotesPage />} />
              <Route path="/quotes/:id" element={<QuoteBuilderPage />} />
              <Route path="/clients" element={<ClientsPage />} />
              <Route path="/settings" element={<div className="text-white">Configurações (Em breve)</div>} />
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
            </Route>
          </Route>

          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
