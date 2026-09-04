import sqlalchemy as db
import sqlalchemy.orm as orm
engine = db.create_engine('sqlite:///orm_db.db')
conn = engine.connect()
Base = orm.declarative_base()

class Produto(Base):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    preco = db.Column(db.Integer)
    # Quantidade de produto
    qtd = db.Column(db.Integer)
    # Definindo relações (importante: uselist=False -> um produto pode ser apenas um eletronico)
    eletronico = orm.relationship("Eletronico", back_populates="produto")

class Eletronico(Base):
    __tablename__ = 'eletronico'
    id = db.Column(db.Integer, primary_key=True)
    # Tipo do produto 
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.id'))
    marca = db.Column(db.String)
    modelo = db.Column(db.String)
    # Definindo relações (importante: uselist=False -> o produto pode )
    produto = orm.relationship("Produto", back_populates="eletronico", uselist=False)
    # Definindo relações com os subtipos
    eletronicodomestico = orm.relationship("EletronicoDomestico", back_populates="eletronico", uselist=False)
    eletronicoindustrial = orm.relationship("EletronicoIndustrial", back_populates="eletronico", uselist=False)
    eletronicointeligente = orm.relationship("EletronicoInteligente", back_populates="eletronico", uselist=False)

# Subcategorias de Eletronicos
# -----------------------------------------
class EletronicoDomestico(Base):
    __tablename__ = 'eletronicodomestico'
    id = db.Column(db.Integer, primary_key=True)
    id_eletronico = db.Column(db.Integer, db.ForeignKey('eletronico.id'), unique=True)
    cor = db.Column(db.String)
    material = db.Column(db.String)
    eletronico = orm.relationship("Eletronico", back_populates="eletronicodomestico", uselist=False)

class EletronicoIndustrial(Base):
    __tablename__ = 'eletronicoindustrial'
    id = db.Column(db.Integer, primary_key=True)
    id_eletronico = db.Column(db.Integer, db.ForeignKey('eletronico.id'), unique=True)
    nicho = db.Column(db.String)
    material = db.Column(db.String)
    eletronico = orm.relationship("Eletronico", back_populates="eletronicoindustrial", uselist=False)

class EletronicoInteligente(Base):
    __tablename__ = 'eletronicointeligente'
    id = db.Column(db.Integer, primary_key=True)
    id_eletronico = db.Column(db.Integer, db.ForeignKey('eletronico.id'), unique=True)
    conectividade = db.Column(db.Boolean)
    eletronico = orm.relationship("Eletronico", back_populates="eletronicointeligente", uselist=False)
# -----------------------------------------

Base.metadata.create_all(engine)
Session = orm.sessionmaker(bind=engine)