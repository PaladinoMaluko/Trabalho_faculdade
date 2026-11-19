
const RelatorioView = {
  template: '#template-relatorio-view',

  data() {
    return {
      carregando: false,
      erro: '',

      faturamento: 0,
      maisVendido: null,
      vendasPorProduto: [],
      movimentacoes: [],
      produtos: [],
      eletronicos: [],

      dataGeracao: '',
    };
  },

  computed: {
    totalProdutos() {
      return this.produtos.length;
    },

    totalEletronicos() {
      return this.eletronicos.length;
    },

    totalUnidadesVendidas() {
      return this.vendasPorProduto.reduce(
        (total, venda) => total + Number(venda.total_vendido || 0),
        0
      );
    },

    totalDomesticos() {
      return this.eletronicos.filter(e => e.eletronicodomestico).length;
    },

    totalIndustriais() {
      return this.eletronicos.filter(e => e.eletronicoindustrial).length;
    },

    totalInteligentes() {
      return this.eletronicos.filter(e => e.eletronicointeligente).length;
    },
  },

  methods: {
    async gerar() {
      this.carregando = true;
      this.erro = '';

      try {
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

        this.faturamento = Number(
          faturamento.faturamento_total || 0
        );

        this.maisVendido = maisVendido;
        this.vendasPorProduto = vendasPorProduto || [];
        this.movimentacoes = movimentacoes || [];
        this.produtos = produtos || [];
        this.eletronicos = eletronicos || [];

        this.dataGeracao = new Date().toLocaleString('pt-BR');

      } catch (e) {
        this.erro = e.message;
      } finally {
        this.carregando = false;
      }
    },

    moeda(valor) {
      return Number(valor || 0).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL',
      });
    },

    exportarPDF() {
      window.print();
    },
  },

  mounted() {
    this.gerar();
  },
};
