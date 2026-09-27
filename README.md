# Trabalho faculdade
Trabalho da faculdade sobre como resolver um problema real com banco de dados e API

# Sistema de Gestão de Produtos

Trabalho prático do Grau A — Disciplina de Implementação de Software.

**Integrantes:**
- Bárbara Doering Barcellos
- Leticia Haussmann Nor
- Mateus Rodolfo Costa

---

## Sobre o Projeto

Sistema completo de gestão de produtos, eletrônicos e vendas, desenvolvido para resolver problemas reais de controle de estoque e rastreabilidade em uma empresa.

O projeto é composto por duas partes:

1. **API REST** — backend em Flask + SQLAlchemy que persiste os dados em SQLite.
2. **Aplicação Cliente** — interface em terminal que consome a API via HTTP/JSON usando a biblioteca `requests`.

---

## Problema Identificado

- Falta de controle centralizado de produtos.
- Ausência de histórico de operações (quem alterou o quê, quando).
- Falta de relatórios para tomada de decisão.

## Solução

- **API REST** com CRUD completo para Produto, Eletronico e Venda.
- **Log de auditoria automático** — toda operação de escrita gera um registro.
- **Relatórios agregados** — faturamento total, produto mais vendido, vendas por produto e movimentações por tipo.
- **Cliente terminal** com menus interativos e validação de entrada.

---

**Tecnologias utilizadas:**
- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
- requests (cliente HTTP)

---

## Estrutura do Projeto

Trabalho_faculdade

    ├── app/ # API REST
    │ ├── init.py # Fabrica da aplicacao Flask
    │ ├── models.py # Modelos do banco (SQLAlchemy)
    │ └── routes.py # Rotas da API + logica de negocio
    ├── cliente/ # Aplicacao cliente (terminal)
    │ ├── init.py
    │ ├── api_client.py # Funcoes que consomem a API
    ├── tests/
    │ ├── test_api.py # Verificação do funcionamento do projeto
    ├── instance/ # Banco de dados (gerado automaticamente)
    ├── run.py # Ponto de entrada da API
    ├── requirements.txt # Dependencias do projeto
    ├── README.md
    └── cliente.py # Menu principal e submenus


---

## Modelo de Dados

**7 entidades principais:**

| Entidade | Descricao |
| :--- | :--- |
| `Produto` | Produto generico (nome, preco, quantidade em estoque) |
| `Eletronico` | Especializacao de Produto (marca, modelo) |
| `EletronicoDomestico` | Subtipo (cor, material) |
| `EletronicoIndustrial` | Subtipo (nicho, material) |
| `EletronicoInteligente` | Subtipo (conectividade) |
| `Venda` | Registro de venda (quantidade, preco unitario, valor total) |
| `Registro` | Log de auditoria (tipo de evento, entidade, descricao) |

**Relacionamentos:**
- `Produto 1 : 0..1 Eletronico` — um produto pode ser um eletronico, mas nao e obrigatorio.
- `Eletronico 1 : 0..1 Subtipo` — um eletronico pode ter no maximo um dos tres subtipos (garantido por `unique=True`).
- `Produto 1 : N Venda` — um produto pode ter varias vendas.
- `Registro` — entidade independente (log historico, sem FK).

---

## Como Rodar

### Pre-requisitos

- Python 3.10 ou superior
- pip

### 1. Clonar o repositorio

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
A API estara disponivel em http://127.0.0.1:5000.
```

### 5. Rodar o cliente (em outro terminal)
Com o venv ativado:

```bash
python cliente/main.py
```
O menu interativo abrira no terminal.
