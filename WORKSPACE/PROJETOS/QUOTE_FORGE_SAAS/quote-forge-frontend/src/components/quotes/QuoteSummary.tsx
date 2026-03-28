interface QuoteSummaryProps {
  subtotal: number;
  tax: number;
  total: number;
  currency: string;
}

export function QuoteSummary({ subtotal, tax, total, currency }: QuoteSummaryProps) {
  const format = (val: number) => 
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency }).format(val);

  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 p-6 flex flex-col w-full max-w-sm ml-auto">
      <div className="flex justify-between py-2 text-slate-400">
        <span>Subtotal</span>
        <span className="font-mono">{format(subtotal)}</span>
      </div>
      <div className="flex justify-between py-2 text-slate-400 border-b border-slate-700">
        <span>Impostos (Taxas)</span>
        <span className="font-mono">{format(tax)}</span>
      </div>
      <div className="flex justify-between py-4 text-white text-lg font-bold">
        <span>Total</span>
        <span className="font-mono text-blue-400">{format(total)}</span>
      </div>
    </div>
  );
}
