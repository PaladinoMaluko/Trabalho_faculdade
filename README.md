# Trabalho faculdade
Trabalho da faculdade sobre como resolver um problema real com banco de dados e API.

# Sistema de Gestão de Produtos
Trabalho prático do Grau A — Disciplina de Implementação de Software.

**Integrantes:**
- Bárbara Doering Barcellos
- Leticia Haussmann Nor
- Mateus Rodolfo Costa

---

## Sobre o Projeto

Sistema completo de gestão de produtos, eletrônicos e vendas, desenvolvido para resolver problemas reais de controle de estoque e rastreabilidade em uma empresa.

O projeto é composto por três partes:

1. **API REST** — backend em Flask + SQLAlchemy que persiste os dados em SQLite.
2. **Interface Web (Frontend)** — dashboard moderno em Vue.js 3 para gestão visual dos dados e emissão de relatórios.
3. **Aplicação Cliente (Terminal)** — interface via linha de comando que também consome a API.

---

## Problema Identificado

- Falta de controle centralizado de produtos.
- Ausência de histórico de operações (quem alterou o quê, quando).
- Falta de relatórios visuais para tomada de decisão.

## Solução

- **API REST** com CRUD completo para Produto, Eletronico e Venda.
- **Log de auditoria automático** — toda operação de escrita gera um registro no banco.
- **Relatórios agregados** — faturamento total, produto mais vendido, vendas por produto e movimentações por tipo.
- **Frontend Web** — interface interativa com cadastro de produtos, listagem em tempo real, venda e dashboard gerencial com exportação de relatórios.
- **Cliente terminal** com menus interativos e validação de entrada.

---

**Tecnologias utilizadas:**

*Backend e Cliente:*
- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- SQLite
- requests (cliente HTTP)

*Frontend:*
- Vue.js 3 (via CDN)
- HTML5 / CSS3
- JavaScript (ES6+)
- Marked.js (renderização de Markdown)

---

## Estrutura do Projeto

```text
Trabalho_faculdade/
├── app/                  # API REST
│   ├── __init__.py       # Fábrica da aplicação Flask
│   ├── models.py         # Modelos do banco (SQLAlchemy)
│   └── routes.py         # Rotas da API + lógica de negócio
├── front/                # Interface Web (Vue.js)
│   ├── index.html        # Estrutura e templates HTML
│   ├── style.css         # Estilização e dashboard
│   ├── app.js            # Configuração de conexão com a API
│   ├── main.js           # Instância principal do Vue
│   ├── ProdutoForm.js    # Componente de cadastro
│   ├── ProdutoList.js    # Componente de listagem
│   └── RelatorioView.js  # Componente do dashboard de relatórios
├── cliente/              # Aplicação cliente (terminal)
│   ├── __init__.py
│   └── api_client.py     # Funções que consomem a API
├── tests/
│   └── test_api.py       # Verificação do funcionamento do projeto
├── instance/             # Banco de dados (gerado automaticamente)
├── run.py                # Ponto de entrada da API
├── requirements.txt      # Dependências do projeto
├── README.md
└── cliente.py            # Menu principal e submenus (terminal)
---
```

## Modelo de Dados

**7 entidades principais:**

| Entidade | Descrição |
| :--- | :--- |
| `Produto` | Produto genérico (nome, preço, quantidade em estoque) |
| `Eletronico` | Especialização de Produto (marca, modelo) |
| `EletronicoDomestico` | Subtipo (cor, material) |
| `EletronicoIndustrial` | Subtipo (nicho, material) |
| `EletronicoInteligente` | Subtipo (conectividade) |
| `Venda` | Registro de venda (quantidade, preço unitário, valor total) |
| `Registro` | Log de auditoria (tipo de evento, entidade, descrição) |

**Relacionamentos:**
- `Produto 1 : 0..1 Eletronico` — um produto pode ser um eletrônico, mas não é obrigatório.
- `Eletronico 1 : 0..1 Subtipo` — um eletrônico pode ter no máximo um dos três subtipos.
- `Produto 1 : N Venda` — um produto pode ter várias vendas.
- `Registro` — entidade independente (log histórico, sem FK).

---

## Como Rodar

### Pré-requisitos
- Python 3.10 ou superior
- Navegador Web atualizado (Chrome, Firefox, Edge, etc.)
- pip

### 1. Clonar o repositório
```bash
git clone <url-do-repositorio>
cd Trabalho_faculdade
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```


### 4. Rodar a API
Em um terminal (com o venv ativado):
```bash
python run.py
```
A API estará disponível em *http://127.0.0.1:5000*.

### 5. Rodar a Interface Web (Frontend)
Com a API rodando, abra o arquivo `front/index.html` no seu navegador de preferência.

> **Dica:** Para uma experiência melhor durante o desenvolvimento, utilize a extensão **Live Server** no VS Code para abrir o `index.html`.

### 6. Rodar o cliente em Terminal (Opcional)
Se desejar usar a interface de linha de comando, abra outro terminal (com o venv ativado) e execute:
```bash
python cliente/main.py
```
O menu interativo abrirá no terminal.

---

## Funcionalidades da Interface Web

- **Cadastro Inteligente:** Formulário que se adapta caso o produto seja um eletrônico (com campos específicos para Doméstico, Industrial ou Inteligente).
- **Gestão de Estoque e Vendas:** Ações rápidas na tabela para registrar uma venda ou excluir um item.
- **Dashboard de Relatórios:** Visão gerencial com indicadores (cards) de faturamento, quantidade de produtos, produto mais vendido e um resumo detalhado das movimentações.
- **Exportação:** O relatório pode ser impresso ou salvo como PDF diretamente pelo navegador.