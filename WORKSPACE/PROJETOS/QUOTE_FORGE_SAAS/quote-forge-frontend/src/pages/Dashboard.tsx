

export const Dashboard = () => {
  return (
    <div className="space-y-6">
      <div className="bg-dark-card border border-dark-border p-8 rounded-2xl shadow-sm">
        <h1 className="text-3xl font-bold text-white mb-2">Bem-vindo ao Quote Forge</h1>
        <p className="text-slate-400">Seu ambiente de geração de orçamentos soberanos está pronto.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          { label: 'Orçamentos Ativos', value: '0', color: 'text-primary' },
          { label: 'Templates Salvos', value: '1', color: 'text-green-500' },
          { label: 'Snapshots Gerados', value: '0', color: 'text-orange-500' },
        ].map((stat) => (
          <div key={stat.label} className="bg-dark-card border border-dark-border p-6 rounded-2xl">
            <p className="text-sm text-slate-400 font-medium mb-1">{stat.label}</p>
            <p className={`text-3xl font-bold ${stat.color}`}>{stat.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
