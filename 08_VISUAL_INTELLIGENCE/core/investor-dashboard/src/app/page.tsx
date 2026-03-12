import AntiGravityHero from "@/components/ui/particle-effect-for-hero";

export default function Home() {
  return (
    <main className="min-h-screen bg-black">
      <AntiGravityHero />

      {/* Investor Info Section */}
      <section className="relative z-20 py-24 px-6 md:px-12 bg-black text-white">
        <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-12">
          <div className="p-8 border border-white/10 rounded-2xl bg-white/5 hover:bg-white/10 transition-colors">
            <h3 className="text-5xl font-bold mb-4">95%</h3>
            <p className="text-white/60 font-light">Redução média no consumo de tokens através do Delta Sync e Cognitive Caching.</p>
          </div>
          <div className="p-8 border border-white/10 rounded-2xl bg-white/5 hover:bg-white/10 transition-colors">
            <h3 className="text-5xl font-bold mb-4">0%</h3>
            <p className="text-white/60 font-light">Índice de alucinação técnica verificado pelo Neuro Consilium e G7 VibeCode.</p>
          </div>
          <div className="p-8 border border-white/10 rounded-2xl bg-white/5 hover:bg-white/10 transition-colors">
            <h3 className="text-5xl font-bold mb-4">100%</h3>
            <p className="text-white/60 font-light">Soberania de dados garantida pelo EVO-04.5 Context Shield e ResistOS.</p>
          </div>
        </div>

        <div className="mt-32 max-w-4xl mx-auto space-y-16">
          <div className="text-center space-y-4">
            <h2 className="text-4xl md:text-6xl font-bold tracking-tight">Arquitetura Soberana</h2>
            <p className="text-white/50 text-xl font-light">Do Caos à Engenharia Determinística.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="p-8 bg-white/5 rounded-3xl border border-white/10 space-y-4 hover:border-blue-500/50 transition-all group">
              <div className="w-12 h-12 bg-blue-500/20 rounded-xl flex items-center justify-center text-blue-400 group-hover:scale-110 transition-transform">
                <span className="font-bold">E5</span>
              </div>
              <h4 className="text-xl font-bold text-white">EVO-05: WASM Sandbox <span className="text-[10px] text-blue-400/50 ml-2">INFRA GENESISCORE</span></h4>
              <p className="text-white/60 text-sm leading-relaxed">Ambiente isolado de execução com Fuel Metering. Garante que qualquer código gerado pela IA seja testado em uma "jaula de ouro" antes de tocar o host.</p>
            </div>
            <div className="p-8 bg-white/5 rounded-3xl border border-white/10 space-y-4 hover:border-blue-500/50 transition-all group">
              <div className="w-12 h-12 bg-blue-500/20 rounded-xl flex items-center justify-center text-blue-400 group-hover:scale-110 transition-transform">
                <span className="font-bold">E1</span>
              </div>
              <h4 className="text-xl font-bold text-white">EVO-01: Zero-Trust <span className="text-[10px] text-blue-400/50 ml-2">INFRA GENESISCORE</span></h4>
              <p className="text-white/60 text-sm leading-relaxed">Handshake de segurança obrigatório. Nenhum agente ou serviço externo acessa a infraestrutura sem certificação atômica.</p>
            </div>
            <div className="p-8 bg-white/5 rounded-3xl border border-white/10 space-y-4 hover:border-blue-500/50 transition-all group">
              <div className="w-12 h-12 bg-blue-500/20 rounded-xl flex items-center justify-center text-blue-400 group-hover:scale-110 transition-transform">
                <span className="font-bold">G7</span>
              </div>
              <h4 className="text-xl font-bold text-white">G7: VibeCode DSL <span className="text-[10px] text-blue-400/50 ml-2">INFRA GENESISCORE</span></h4>
              <p className="text-white/60 text-sm leading-relaxed">Validação de lógica formal. O código só é gravado se passar pelo crivo matemático da nossa Linguagem Soberana Proprietária.</p>
            </div>
            <div className="p-8 bg-white/5 rounded-3xl border border-white/10 space-y-4 hover:border-blue-500/50 transition-all group">
              <div className="w-12 h-12 bg-blue-500/20 rounded-xl flex items-center justify-center text-blue-400 group-hover:scale-110 transition-transform">
                <span className="font-bold">NC</span>
              </div>
              <h4 className="text-xl font-bold text-white">Neuro Consilium</h4>
              <p className="text-white/60 text-sm leading-relaxed">Deliberação multi-agente. Kimi, Inception, OpenAI e Claude trabalham em consenso para eliminar alucinações.</p>
            </div>
          </div>

          <div className="py-20 border-y border-white/5">
            <div className="max-w-3xl mx-auto text-center space-y-8">
              <h3 className="text-2xl font-mono text-white/40 tracking-[0.3em] uppercase">A Saga do Programador</h3>
              <p className="text-2xl md:text-3xl font-light italic text-white/80 leading-snug">
                "Antes do Antigravity, vivíamos no caos das alucinações e do consumo desenfreado de tokens. Hoje, operamos com Soberania Determinística."
              </p>
              <div className="flex justify-center gap-4">
                <div className="h-px w-12 bg-white/20 self-center"></div>
                <span className="text-white/40 text-sm italic">O Fim da IA Volátil</span>
                <div className="h-px w-12 bg-white/20 self-center"></div>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-32 text-center">
          <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-8">Pronto para a Era Soberana?</h2>
          <p className="text-white/50 max-w-2xl mx-auto mb-12">O Antigravity não é apenas uma ferramenta de IA. É uma infraestrutura de engenharia autônoma projetada para operações corporativas de alto risco.</p>
          <button className="px-12 py-5 bg-white text-black rounded-full font-bold hover:bg-white/90 transition-all text-lg">
            Baixar Bíblia de Evolução
          </button>
        </div>
      </section>

      <footer className="relative z-20 py-12 border-t border-white/5 text-center text-white/20 text-xs tracking-widest uppercase">
        &copy; 2026 Antigravity Sovereign Intelligence. Todos os Direitos Reservados.
      </footer>
    </main>
  );
}
