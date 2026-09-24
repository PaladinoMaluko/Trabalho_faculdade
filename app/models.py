from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Produto(db.Model):
    """Representa um produto genérico."""
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    preco = db.Column(db.Integer)
    # Quantidade de produto
    qtd = db.Column(db.Integer)

    # Definindo relações (importante: um produto pode ser apenas um eletronico)
    eletronico = db.relationship("Eletronico", back_populates="produto", uselist=False)
    vendas = db.relationship("Venda", back_populates="produto")


    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "qtd": self.qtd
        }


class Eletronico(db.Model):
    """Representa um tipo de produto."""
    __tablename__ = 'eletronico'
    id = db.Column(db.Integer, primary_key=True)
    # Tipo do produto 
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.id'))
    marca = db.Column(db.String)
    modelo = db.Column(db.String)

    # Definindo relações (importante: um produto pode ser um eletronico ou não)
    produto = db.relationship("Produto", back_populates="eletronico", uselist=False)
    # Definindo relações com os subtipos
    eletronicodomestico = db.relationship("EletronicoDomestico", back_populates="eletronico", uselist=False)
    eletronicoindustrial = db.relationship("EletronicoIndustrial", back_populates="eletronico", uselist=False)
    eletronicointeligente = db.relationship("EletronicoInteligente", back_populates="eletronico", uselist=False)

    def to_dict(self):
        return {
            "id": self.id,
            "id_produto": self.id_produto,
            "marca": self.marca,
            "modelo": self.modelo
        }


# Subcategorias de Eletronicos
# -----------------------------------------
class EletronicoDomestico(db.Model):
    """Representa um subtipo de produto do tipo eletronico."""
    __tablename__ = 'eletronicodomestico'
    id = db.Column(db.Integer, primary_key=True)
    id_eletronico = db.Column(db.Integer, db.ForeignKey('eletronico.id'), unique=True)
    cor = db.Column(db.String)
    material = db.Column(db.String)

    # Definindo relações
    eletronico = db.relationship("Eletronico", back_populates="eletronicodomestico", uselist=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "id_eletronico": self.id_eletronico,
            "cor": self.cor,
            "material": self.material
        }


class EletronicoIndustrial(db.Model):
    """Representa um subtipo de produto do tipo eletronico."""
    __tablename__ = 'eletronicoindustrial'
    id = db.Column(db.Integer, primary_key=True)
    id_eletronico = db.Column(db.Integer, db.ForeignKey('eletronico.id'), unique=True)
    nicho = db.Column(db.String)
    material = db.Column(db.String)

    # Definindo relações
    eletronico = db.relationship("Eletronico", back_populates="eletronicoindustrial", uselist=False)

    def to_dict(self):
        return {
            "id": self.id,
            "id_eletronico": self.id_eletronico,
            "nicho": self.nicho,
            "material": self.material
        }


class EletronicoInteligente(db.Model):
    """Representa um subtipo de produto do tipo eletronico."""
    __tablename__ = 'eletronicointeligente'
    id = db.Column(db.Integer, primary_key=True)
    id_eletronico = db.Column(db.Integer, db.ForeignKey('eletronico.id'), unique=True)
    conectividade = db.Column(db.Boolean)

    # Definindo relações
    eletronico = db.relationship("Eletronico", back_populates="eletronicointeligente", uselist=False)

    def to_dict(self):
        return {
            "id": self.id,
            "id_eletronico": self.id_eletronico,
            "conectividade": self.conectividade
        }
# -----------------------------------------


class Registro(db.Model):
    """Registros dos eventos executados."""
    __tablename__ = 'registro'
    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    tipo_evento = db.Column(db.String, nullable=False)
    entidade = db.Column(db.String, nullable=False)
    id_entidade = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "data_hora": self.data_hora.isoformat() if self.data_hora else None,
            "tipo_evento": self.tipo_evento,
            "entidade": self.entidade,
            "id_entidade": self.id_entidade,
            "descricao": self.descricao
        }

class Venda(db.Model):
    """Registros das vendas."""
    __tablename__ = 'venda'
    id = db.Column(db.Integer, primary_key=True)
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Integer, nullable=False)
    data_venda = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    valor_total = db.Column(db.Integer)  # opcional

    produto = db.relationship("Produto", back_populates="vendas")

    def to_dict(self):
        return {
            "id": self.id,
            "id_produto": self.id_produto,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
            "data_venda": self.data_venda.isoformat() if self.data_venda else None,
            "valor_total": self.valor_total
        }

