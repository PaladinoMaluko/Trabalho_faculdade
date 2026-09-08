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

    # Definindo relações (importante: uselist=False -> um produto pode ser apenas um eletronico)
    eletronico = orm.relationship("Eletronico", back_populates="produto", uselist=False)


class Eletronico(Base):
    """Representa um tipo de produto."""
    __tablename__ = 'eletronico'
    id = db.Column(db.Integer, primary_key=True)
    # Tipo do produto 
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.id'))
    marca = db.Column(db.String)
    modelo = db.Column(db.String)

    # Definindo relações (importante: uselist=False -> o produto pode ser um eletronico ou não)
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

    # Feche a sessão 
    session.close()