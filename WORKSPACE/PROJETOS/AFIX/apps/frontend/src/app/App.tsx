import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from '@/widgets/Layout';
import { DashboardPage } from '@/pages/Dashboard';
import { LeadsPage } from '@/pages/Leads';

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/leads" element={<LeadsPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
