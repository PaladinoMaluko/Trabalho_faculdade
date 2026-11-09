const ProdutoList = {
  // ---------- Template (o que aparece na tela) ----------
  template: '#template-produto-list',

  // props: dados que vêm do componente 
  props: {
    produtos: { type: Array, default: () => [] },
  },

  methods: {
    // Esta função "acha" o tipo a partir do eletronico já juntado pelo pai
    tipo(p) {
      const e = p.eletronico;
      if (!e) return 'Genérico';
      if (e.eletronicodomestico) return 'Eletrônico Doméstico';
      if (e.eletronicoindustrial) return 'Eletrônico Industrial';
      if (e.eletronicointeligente) return 'Eletrônico Inteligente';
      return 'Eletrônico (sem subtipo)';
    },

    detalhes(p) {
      const e = p.eletronico;
      if (!e) return '—';
      const base = `${e.marca} ${e.modelo}`;
      const d = e.eletronicodomestico;
      if (d) return `${base} • Cor: ${d.cor || '—'} • Material: ${d.material || '—'}`;
      const i = e.eletronicoindustrial;
      if (i) return `${base} • Nicho: ${i.nicho || '—'} • Material: ${i.material || '—'}`;
      const s = e.eletronicointeligente;
      if (s) return `${base} • Conectividade: ${s.conectividade ? 'Sim' : 'Não'}`;
      return base;
    },

    moeda: formatarMoeda,   // reaproveita o helper global
  },

};