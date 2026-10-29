const ProdutoList = {
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

  template: `
    <div class="produto-list">
      <h2>Produtos cadastrados</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nome</th>
            <th>Tipo</th>
            <th>Preço</th>
            <th>Estoque</th>
            <th>Detalhes</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in produtos" :key="p.id">
            <td>{{ p.id }}</td>
            <td>{{ p.nome }}</td>
            <td>{{ tipo(p) }}</td>
            <td>{{ moeda(p.preco) }}</td>
            <td>{{ p.qtd }}</td>
            <td>{{ detalhes(p) }}</td>
            <td class="acoes-celula">
              <button @click="$emit('vender', p)">Vender</button>
              <button class="perigo" @click="$emit('deletar', p)">Excluir</button>
            </td>
          </tr>
          <tr v-if="produtos.length === 0">
            <td colspan="7" class="vazio">Nenhum produto cadastrado ainda.</td>
          </tr>
        </tbody>
      </table>
    </div>
  `,
};