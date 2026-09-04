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
    id_produto = db.Column(db.Integer, db.ForeignKey('Produto.id'))
    marca = db.Column(db.String)
    modelo = db.Column(db.String)
    # Definindo relações (importante: uselist=False -> o produto pode )
    produto = orm.relationship("Produto", back_populates="eletronico", uselist=False)
    
class EletroDomestico(Base):
    __tablename__ = 'eletrodomestico'
    id = db.Column(db.Integer, primary_key=True)
    id_eletronico = db.Column(db.Integer, db.ForeignKey('Eletronico.id'))
    cor = db.Column(db.String)
    material = db.Column(db.String)



Base.metadata.create_all(engine)
Session = orm.sessionmaker(bind=engine)