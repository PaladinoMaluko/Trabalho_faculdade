const RelatorioView = {
  // ---------- Template (o que aparece na tela) ----------
  template: '#template-relatorio-view',
  data() {
    return {
      carregando: false,
      erro: '',
      markdown: '',
    };
  },

  methods: {
    async gerar() {
      this.carregando = true;
      this.erro = '';
      try {
        // Promise.all = dispara tudo em paralelo e espera o conjunto
        const [
          faturamento,
          maisVendido,
          vendasPorProduto,
          movimentacoes,
          produtos,
          eletronicos,
        ] = await Promise.all([
          api('GET', '/relatorios/faturamento-total'),
          api('GET', '/relatorios/produto-mais-vendido'),
          api('GET', '/relatorios/vendas-por-produto'),
          api('GET', '/relatorios/movimentacoes-por-tipo'),
          api('GET', '/produtos'),
          api('GET', '/eletronicos'),
        ]);

        this.markdown = this.montarMarkdown({
          faturamento, maisVendido, vendasPorProduto,
          movimentacoes, produtos, eletronicos,
        });
      } catch (e) {
        this.erro = e.message;
      } finally {
        this.carregando = false;
      }
    },

    // Monta a string Markdown 
    montarMarkdown(d) {
      const agora = new Date().toLocaleString('pt-BR');
      const linhas = [];
      const push = (...args) => linhas.push(...args);

      push('# Relatório do Sistema de Gestão de Produtos', '');
      push(`_Gerado em ${agora}_`, '');

      // ----- Resumo do catálogo -----
      push('## Resumo do catálogo', '');
      push(`- **Total de produtos:** ${d.produtos.length}`);
      push(`- **Total de eletrônicos:** ${d.eletronicos.length}`);

      const cont = { domestico: 0, industrial: 0, inteligente: 0 };
      d.eletronicos.forEach(e => {
        if (e.eletronicodomestico) cont.domestico++;
        else if (e.eletronicoindustrial) cont.industrial++;
        else if (e.eletronicointeligente) cont.inteligente++;
      });
      push(`  - Domésticos: ${cont.domestico}`);
      push(`  - Industriais: ${cont.industrial}`);
      push(`  - Inteligentes: ${cont.inteligente}`, '');

      // ----- Faturamento -----
      push('## Faturamento', '');
      push(`**Total:** ${formatarMoeda(d.faturamento.faturamento_total)}`, '');

      // ----- Produto mais vendido -----
      push('## Produto mais vendido', '');
      if (d.maisVendido && d.maisVendido.nome) {
        push(`- **Produto:** ${d.maisVendido.nome} (ID ${d.maisVendido.id})`);
        push(`- **Unidades vendidas:** ${d.maisVendido.total_vendido}`);
        push(`- **Faturamento gerado:** ${formatarMoeda(d.maisVendido.faturamento)}`);
      } else {
        push('_Nenhuma venda registrada ainda._');
      }
      push('');

      // ----- Vendas por produto -----
      push('## Vendas por produto', '');
      if (d.vendasPorProduto.length) {
        push('| Produto | Unidades | Faturamento |');
        push('| :--- | ---: | ---: |');
        d.vendasPorProduto.forEach(v => {
          push(`| ${v.nome} | ${v.total_vendido} | ${formatarMoeda(v.faturamento)} |`);
        });
      } else {
        push('_Sem vendas registradas._');
      }
      push('');

      // ----- Movimentações por tipo -----
      push('## Movimentações por tipo de evento', '');
      if (d.movimentacoes.length) {
        push('| Tipo | Total |');
        push('| :--- | ---: |');
        d.movimentacoes.forEach(m => push(`| ${m.tipo_evento} | ${m.total} |`));
      } else {
        push('_Sem movimentações registradas._');
      }
      push('');

      return linhas.join('\n');
    },

    parseMarkdown(texto) {
      // Verifica se a biblioteca marked carregou e converte o texto
      if (typeof marked !== 'undefined') {
        return marked.parse(texto);
      }
      return texto;
    },

    async copiar() {
      try {
        await navigator.clipboard.writeText(this.markdown);
      } catch {
        // Fallback p/ quando aberto via file:// (clipboard API exige contexto seguro)
        const pre = this.$refs.preview;
        const range = document.createRange();
        range.selectNode(pre);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);
        document.execCommand('copy');
      }
      alert('Relatório copiado para a área de transferência!');
    },

    baixar() {
      const blob = new Blob([this.markdown], { type: 'text/markdown;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'relatorio.md';
      a.click();
      URL.revokeObjectURL(url);
    },
  },

  mounted() {
    // `mounted` roda automaticamente quando o componente aparece na tela
    this.gerar();
  },

};