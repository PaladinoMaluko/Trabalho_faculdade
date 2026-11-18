const app = Vue.createApp({
  data() {
    return {
      aba: 'produtos',
      produtos: [],
      eletronicos: [],
      carregando: false,
      erro: '',
    };
  },

  computed: {
    // Junta produto + eletrônico
    produtosCompletos() {
      const mapa = {};

      this.eletronicos.forEach(e => {
        mapa[e.id_produto] = e;
      });

      return this.produtos.map(p => ({
        ...p,
        eletronico: mapa[p.id] || null,
      }));
    },
  },

  methods: {
    // Carrega produtos e eletrônicos da API
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

    // Exclui um produto
    async deletarProduto(produto) {
      if (!confirm(`Excluir "${produto.nome}"?`)) return;

      try {
        // Se tiver eletrônico, apaga primeiro
        if (produto.eletronico) {
          await api('DELETE', `/eletronicos/${produto.eletronico.id}`);
        }

        await api('DELETE', `/produtos/${produto.id}`);

        await this.carregar();

      } catch (e) {
        alert('Erro ao excluir: ' + e.message);
      }
    },

    // Realiza uma venda
    async venderProduto(produto) {
      const qtdStr = prompt(
        `Quantas unidades de "${produto.nome}" vender?`,
        1
      );

      if (!qtdStr) return;

      const quantidade = parseInt(qtdStr, 10);

      if (!quantidade || quantidade <= 0) {
        alert('Quantidade inválida.');
        return;
      }

      const precoStr = prompt('Preço unitário (R$):', produto.preco);

      if (!precoStr) return;

      const precoUnitario = Number(precoStr);

      if (!precoUnitario || precoUnitario <= 0) {
        alert('Preço inválido.');
        return;
      }

      try {
        // Envia a venda para o backend
        await api('POST', '/vendas', {
          id_produto: produto.id,
          quantidade,
          preco_unitario: precoUnitario,
        });

        // Recarrega os produtos para atualizar o estoque
        await this.carregar();

        alert('Venda registrada e estoque atualizado!');

      } catch (e) {
        alert('Erro ao registrar venda: ' + e.message);
      }
    },
  },

  mounted() {
    // Carrega os dados ao iniciar a aplicação
    this.carregar();
  },
});
app.component('produto-form', ProdutoForm);

app.component('produto-list', {
  ...ProdutoList,
  emits: ['vender', 'deletar', 'adicionar-estoque'],
});

app.component('relatorio-view', RelatorioView);
// Registra os componentes
app.component('produto-form', ProdutoForm);
app.component('produto-list', ProdutoList);
app.component('relatorio-view', RelatorioView);

// Inicializa a aplicação
app.mount('#app');      