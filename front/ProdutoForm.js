const ProdutoForm = {
  // ---------- Template (o que aparece na tela) ----------
  template: '#template-produto-form',
  data() {
    return {
      produto: {
        nome: '',
        preco: 0,
        qtd: 0,
        ehEletronico: false,
        marca: '',
        modelo: '',
        subtipo: '',     
        cor: '',
        material: '',
        nicho: '',
        conectividade: false,
      },
      salvando: false,
      erro: '',
    };
  },

  methods: {
    // ---------- Validação local antes de chamar a API ----------
    validar() {
      if (!this.produto.nome.trim()) return 'Informe o nome do produto.';
      if (Number(this.produto.preco) < 0) return 'Preço não pode ser negativo.';
      if (Number(this.produto.qtd) < 0) return 'Quantidade não pode ser negativa.';
      if (this.produto.ehEletronico) {
        if (!this.produto.marca.trim()) return 'Informe a marca do eletrônico.';
        if (!this.produto.modelo.trim()) return 'Informe o modelo do eletrônico.';
      }
      return null;
    },

    async salvar() {
      this.erro = '';
      const msg = this.validar();
      if (msg) { this.erro = msg; return; }

      this.salvando = true;
      let produtoCriado = null;

      try {
        // ---------- 1) Cria o Produto ----------
        produtoCriado = await api('POST', '/produtos', {
          nome: this.produto.nome.trim(),
          preco: Number(this.produto.preco),
          qtd:   Number(this.produto.qtd),
        });

        // ---------- 2) Se for eletrônico, cria o Eletronico ----------
        if (this.produto.ehEletronico) {
          const corpo = {
            id_produto: produtoCriado.id,
            marca: this.produto.marca.trim(),
            modelo: this.produto.modelo.trim(),
          };
          if (this.produto.subtipo) {
            corpo.subtipo = this.produto.subtipo;
            if (this.produto.subtipo === 'domestico') {
              corpo.cor = this.produto.cor;
              corpo.material = this.produto.material;
            } else if (this.produto.subtipo === 'industrial') {
              corpo.nicho = this.produto.nicho;
              corpo.material = this.produto.material;
            } else if (this.produto.subtipo === 'inteligente') {
              corpo.conectividade = this.produto.conectividade;
            }
          }

          try {
            await api('POST', '/eletronicos', corpo);
          } catch (e) {
            // "rollback manual": se o eletrônico falhar, apaga o produto órfão.
            // (Nosso backend é stateless entre requisições, então temos que
            //  desfazer na mão — não existe transação HTTP multi-endpoint.)
            try { await api('DELETE', `/produtos/${produtoCriado.id}`); } catch {}
            throw e;
          }
        }

        // ---------- 3) Avisa e limpa o formulário ----------
        this.resetar();
        // $emit dispara um evento que o pai escuta com @criado="carregar"
        this.$emit('criado');
      } catch (e) {
        this.erro = e.message;
      } finally {
        this.salvando = false;
      }
    },

    resetar() {
      this.produto = {
        nome: '', preco: 0, qtd: 0,
        ehEletronico: false, marca: '', modelo: '', subtipo: '',
        cor: '', material: '', nicho: '', conectividade: false,
      };
    },
  },
};