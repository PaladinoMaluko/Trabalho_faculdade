import sqlalchemy as db
import sqlalchemy.orm as orm
engine = db.create_engine('sqlite:///instances/orm_db.db')
Base = orm.declarative_base()

class Produto(Base):
    """Representa um produto genérico."""
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    preco = db.Column(db.Integer)
    # Quantidade de produto
    qtd = db.Column(db.Integer)

    # Definindo relações (importante: um produto pode ser apenas um eletronico)
    eletronico = orm.relationship("Eletronico", back_populates="produto", uselist=False)
    vendas = orm.relationship("Venda", back_populates="produto")


class Eletronico(Base):
    """Representa um tipo de produto."""
    __tablename__ = 'eletronico'
    id = db.Column(db.Integer, primary_key=True)
    # Tipo do produto 
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.id'))
    marca = db.Column(db.String)
    modelo = db.Column(db.String)

    # Definindo relações (importante: um produto pode ser um eletronico ou não)
    produto = orm.relationship("Produto", back_populates="eletronico", uselist=False)
    # Definindo relações com os subtipos
    eletronicodomestico = orm.relationship("EletronicoDomestico", back_populates="eletronico", uselist=False)
    eletronicoindustrial = orm.relationship("EletronicoIndustrial", back_populates="eletronico", uselist=False)
    eletronicointeligente = orm.relationship("EletronicoInteligente", back_populates="eletronico", uselist=False)


# Subcategorias de Eletronicos
# -----------------------------------------
class EletronicoDomestico(Base):
    """Representa um subtipo de produto do tipo eletronico."""
    __tablename__ = 'eletronicodomestico'
    id = db.Column(db.Integer, primary_key=True)
    id_eletronico = db.Column(db.Integer, db.ForeignKey('eletronico.id'), unique=True)
    cor = db.Column(db.String)
    material = db.Column(db.String)

    # Definindo relações
    eletronico = orm.relationship("Eletronico", back_populates="eletronicodomestico", uselist=False)


class EletronicoIndustrial(Base):
    """Representa um subtipo de produto do tipo eletronico."""
    __tablename__ = 'eletronicoindustrial'
    id = db.Column(db.Integer, primary_key=True)
    id_eletronico = db.Column(db.Integer, db.ForeignKey('eletronico.id'), unique=True)
    nicho = db.Column(db.String)
    material = db.Column(db.String)

    # Definindo relações
    eletronico = orm.relationship("Eletronico", back_populates="eletronicoindustrial", uselist=False)


class EletronicoInteligente(Base):
    """Representa um subtipo de produto do tipo eletronico."""
    __tablename__ = 'eletronicointeligente'
    id = db.Column(db.Integer, primary_key=True)
    id_eletronico = db.Column(db.Integer, db.ForeignKey('eletronico.id'), unique=True)
    conectividade = db.Column(db.Boolean)

    # Definindo relações
    eletronico = orm.relationship("Eletronico", back_populates="eletronicointeligente", uselist=False)
# -----------------------------------------


class Registro(Base):
    """Registros dos eventos executados."""
    __tablename__ = 'registro'
    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    tipo_evento = db.Column(db.String, nullable=False)
    entidade = db.Column(db.String, nullable=False)
    id_entidade = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String)

class Venda(Base):
    """Registros das vendas."""
    __tablename__ = 'venda'
    id = db.Column(db.Integer, primary_key=True)
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Integer, nullable=False)
    data_venda = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    valor_total = db.Column(db.Integer)  # opcional

    produto = orm.relationship("Produto", back_populates="vendas")

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    Session = orm.sessionmaker(bind=engine)
    session = Session()

    # # Testes de consultas na tabela Produto 
    # # Execute a consulta para pegar o primeiro resultado 
    # produto = session.query(Produto).filter_by(nome="Celular").first()

    # # Verifique se o produto existe 
    # if produto:
    #     print(produto.id, produto.nome, produto.preco, produto.qtd)
    # else:
    #     print("Produto não encontrado")

    # # Execute a consulta para pegar TODOS os resultados
    # todos_produtos = session.query(Produto).all()

    # for p in todos_produtos:
    #     print(f"ID: {p.id}, Nome: {p.nome}, Preço: {p.preco}, Qtd: {p.qtd}")

    # Testes de consultas de todas tabelas
    # Criando o produto
    produto = Produto(
        nome="Celular", 
        preco=20, 
        qtd=10
    )
    session.add(produto)
    session.commit()

    # Criando o tipo do produto
    eletronico = Eletronico(
        id_produto=produto.id,
        marca="Samsung",
        modelo="Galaxy S23"
    )
    session.add(eletronico)
    session.commit()

    # Criando o subtipo do produto
    domestico = EletronicoDomestico(
        id_eletronico=eletronico.id,
        cor="Preto",
        material="Plástico"
    )
    session.add(domestico)
    session.commit()

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
    session.add(venda)
    session.commit()

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

    session.add_all([registro_venda, registro_criacao])
    session.commit()

    # Consultar todos os registros
    todos_registros = session.query(Registro).order_by(Registro.data_hora).all()
    print(f"Total de registros no log: {len(todos_registros)}")
    for r in todos_registros:
        print(f"  [{r.data_hora}] {r.tipo_evento} em {r.entidade}#{r.id_entidade}: {r.descricao}")

    # Teste de integridade: tentar criar uma venda SEM id_produto (deve falhar)
    print("\n--- Teste de integridade (deve lançar erro) ---")
    try:
        venda_invalida = Venda(quantidade=1, preco_unitario=10)
        session.add(venda_invalida)
        session.commit()
        print("ERRO: venda sem produto foi aceita (não deveria).")
    except Exception as e:
        session.rollback()
        print(f"OK: venda sem produto foi rejeitada. ({type(e).__name__})")

    # Feche a sessão 
    session.close()