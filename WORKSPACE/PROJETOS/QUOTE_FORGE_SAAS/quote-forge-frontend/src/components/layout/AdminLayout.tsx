import { Sidebar } from './Sidebar';
import { Outlet } from 'react-router-dom';

export const AdminLayout = () => {
  return (
    <div className="flex bg-dark-bg min-h-screen">
      <Sidebar />
      <main className="flex-1 flex flex-col overflow-hidden">
        <header className="h-16 border-b border-dark-border bg-dark-card/50 backdrop-blur-md px-8 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-white">Painel de Controle</h2>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm font-medium text-white">Administrador</p>
              <p className="text-xs text-slate-400">ACME Comunicação</p>
            </div>
            <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold">
              A
            </div>
          </div>
        </header>
        <div className="flex-1 overflow-y-auto p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
};
