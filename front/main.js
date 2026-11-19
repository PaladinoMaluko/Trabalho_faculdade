const app = Vue.createApp({
  data() {
    return {
      aba: 'produtos',
      produtos: [],        // lista crua vinda da API
      eletronicos: [],     // lista crua vinda da API
      carregando: false,
      erro: '',
    };
  },

  computed: {
    // Junta produto + eletronico
    produtosCompletos() {
      const mapa = {};
      this.eletronicos.forEach(e => { mapa[e.id_produto] = e; });
      return this.produtos.map(p => ({
        ...p,                          // "spread": copia todos os campos
        eletronico: mapa[p.id] || null,
      }));
    },
  },

  methods: {
    async carregar() {
      this.carregando = true;
      this.erro = '';
      try {
        const [produtos, eletronicos] = await Promise.all([
          api('GET', '/produtos'),
          api('GET', '/eletronicos'),
        ]);
        this.produtos = produtos;
        this.eletronicos = eletronicos;
      } catch (e) {
        this.erro = e.message;
      } finally {
        this.carregando = false;
      }
    },

    async deletarProduto(produto) {
      if (!confirm(`Excluir "${produto.nome}"?`)) return;
      try {
        // Se tiver eletrônico, apaga primeiro para evitar violação de FK
        if (produto.eletronico) {
          await api('DELETE', `/eletronicos/${produto.eletronico.id}`);
        }
        await api('DELETE', `/produtos/${produto.id}`);
        await this.carregar();
      } catch (e) {
        alert('Erro ao excluir: ' + e.message);
      }
    },

    async venderProduto(produto) {
      // Formulário simplificado com prompts — sua colega do CSS pode
      // transformar em modal depois se quiser.
      const qtdStr = prompt(`Quantas unidades de "${produto.nome}" vender?`, 1);
      if (!qtdStr) return;
      const quantidade = parseInt(qtdStr, 10);
      if (!quantidade || quantidade <= 0) { alert('Quantidade inválida.'); return; }

      const precoStr = prompt('Preço unitário (R$):', produto.preco);
      if (!precoStr) return;
      const precoUnitario = Number(precoStr);
      if (!precoUnitario || precoUnitario <= 0) { alert('Preço inválido.'); return; }

      try {
        await api('POST', '/vendas', {
          id_produto: produto.id,
          quantidade,
          preco_unitario: precoUnitario,
        });
        alert('Venda registrada!');
      } catch (e) {
        alert('Erro ao registrar venda: ' + e.message);
      }
    },
  },

  mounted() {
    this.carregar();     // busca dados assim que a página abre
  },
});

// Registra os componentes (mesmos nomes usados no index.html)
app.component('produto-form', ProdutoForm);
app.component('produto-list', ProdutoList);
app.component('relatorio-view', RelatorioView);

app.mount('#app');       