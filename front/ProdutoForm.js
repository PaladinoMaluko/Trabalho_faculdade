const ProdutoForm = {
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

  // ---------- Template (o que aparece na tela) ----------
  // Note o uso de `backticks` (crase) para string multilinha.
  template: `
    <form class="produto-form" @submit.prevent="salvar">
      <h2>Novo Produto</h2>

      <label>
        Nome
        <input v-model="produto.nome" required />
      </label>

      <label>
        Preço (R$)
        <input v-model.number="produto.preco" type="number" min="0" step="1" required />
      </label>

      <label>
        Quantidade em estoque
        <input v-model.number="produto.qtd" type="number" min="0" step="1" required />
      </label>

      <label class="checkbox">
        <input type="checkbox" v-model="produto.ehEletronico" />
        É um eletrônico?
      </label>

      <template v-if="produto.ehEletronico">
        <label>Marca <input v-model="produto.marca" /></label>
        <label>Modelo <input v-model="produto.modelo" /></label>

        <label>
          Subtipo
          <select v-model="produto.subtipo">
            <option value="">— nenhum —</option>
            <option value="domestico">Doméstico</option>
            <option value="industrial">Industrial</option>
            <option value="inteligente">Inteligente</option>
          </select>
        </label>

        <template v-if="produto.subtipo === 'domestico'">
          <label>Cor <input v-model="produto.cor" /></label>
          <label>Material <input v-model="produto.material" /></label>
        </template>

        <template v-if="produto.subtipo === 'industrial'">
          <label>Nicho <input v-model="produto.nicho" /></label>
          <label>Material <input v-model="produto.material" /></label>
        </template>

        <template v-if="produto.subtipo === 'inteligente'">
          <label class="checkbox">
            <input type="checkbox" v-model="produto.conectividade" />
            Possui conectividade
          </label>
        </template>
      </template>

      <p v-if="erro" class="erro">{{ erro }}</p>

      <button type="submit" :disabled="salvando">
        {{ salvando ? 'Salvando...' : 'Cadastrar' }}
      </button>
    </form>
  `,
};