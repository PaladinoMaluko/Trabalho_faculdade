from flask import Flask
from models import (db, Produto, Eletronico, 
                    EletronicoDomestico, EletronicoInteligente, 
                    EletronicoIndustrial, Registro,
                    Venda)

# Teste do uso da api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    # # Testes de consultas na tabela Produto 
    # # Execute a consulta para pegar o primeiro resultado 
    # produto = db.session.query(Produto).filter_by(nome="Celular").first()

    # # Verifique se o produto existe 
    # if produto:
    #     print(produto.id, produto.nome, produto.preco, produto.qtd)
    # else:
    #     print("Produto não encontrado")

    # # Execute a consulta para pegar TODOS os resultados
    # todos_produtos = db.session.query(Produto).all()

    # for p in todos_produtos:
    #     print(f"ID: {p.id}, Nome: {p.nome}, Preço: {p.preco}, Qtd: {p.qtd}")

    # Testes de consultas de todas tabelas
    # Criando o produto
    produto = Produto(
        nome="Celular", 
        preco=20, 
        qtd=10
    )
    db.session.add(produto)
    db.session.commit()

    # Criando o tipo do produto
    eletronico = Eletronico(
        id_produto=produto.id,
        marca="Samsung",
        modelo="Galaxy S23"
    )
    db.session.add(eletronico)
    db.session.commit()

    # Criando o subtipo do produto
    domestico = EletronicoDomestico(
        id_eletronico=eletronico.id,
        cor="Preto",
        material="Plástico"
    )
    db.session.add(domestico)
    db.session.commit()

    # A partir do produto, acessar o eletronico
    print(produto.eletronico.marca)  # Deve imprimir "Samsung"

    # A partir do eletronico, acessar o produto
    print(eletronico.produto.nome)   # Deve imprimir "Celular"

    # A partir do eletronico, acessar o subtipo
    print(eletronico.eletronicodomestico.cor)  # Deve imprimir "Preto"

    # A partir do subtipo, acessar o eletronico
    print(domestico.eletronico.modelo)  # Deve imprimir "Galaxy S23"

    # Testes da tabela Venda
    print("\n--- Testes de Venda ---")

    # Criando uma venda vinculada ao produto "Celular"
    venda = Venda(
        id_produto=produto.id,
        quantidade=3,
        preco_unitario=produto.preco,
        valor_total=3 * produto.preco
    )
    db.session.add(venda)
    db.session.commit()

    # Navegar da venda para o produto
    print(f"Venda #{venda.id} -> Produto: {venda.produto.nome}")
    # Navegar do produto para a lista de vendas
    print(f"Produto '{produto.nome}' tem {len(produto.vendas)} venda(s) registrada(s).")
    for v in produto.vendas:
        print(f"  Venda #{v.id}: {v.quantidade}x a R$ {v.preco_unitario} = R$ {v.valor_total}")

    # Testes da tabela Registro
    print("\n--- Testes de Registro ---")

    # Registrando o evento de venda
    registro_venda = Registro(
        tipo_evento="VENDA",
        entidade="Venda",
        id_entidade=venda.id,
        descricao=f"Venda de {venda.quantidade}x {produto.nome} por R$ {venda.valor_total}"
    )

    # Registrando o evento de criação do produto
    registro_criacao = Registro(
        tipo_evento="CRIACAO",
        entidade="Produto",
        id_entidade=produto.id,
        descricao=f"Produto '{produto.nome}' criado com preço R$ {produto.preco}"
    )

    db.session.add_all([registro_venda, registro_criacao])
    db.session.commit()

    # Consultar todos os registros
    todos_registros = db.session.query(Registro).order_by(Registro.data_hora).all()
    print(f"Total de registros no log: {len(todos_registros)}")
    for r in todos_registros:
        print(f"  [{r.data_hora}] {r.tipo_evento} em {r.entidade}#{r.id_entidade}: {r.descricao}")

    # Teste de integridade: tentar criar uma venda SEM id_produto (deve falhar)
    print("\n--- Teste de integridade (deve lançar erro) ---")
    try:
        venda_invalida = Venda(quantidade=1, preco_unitario=10)
        db.session.add(venda_invalida)
        db.session.commit()
        print("ERRO: venda sem produto foi aceita (não deveria).")
    except Exception as e:
        db.session.rollback()
        print(f"OK: venda sem produto foi rejeitada. ({type(e).__name__})")

    # Feche a sessão 
    db.session.remove()