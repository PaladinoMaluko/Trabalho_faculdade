from flask import Flask
from flask_cors import CORS  
from app.models import (db, Produto, Eletronico, 
                    EletronicoDomestico, EletronicoInteligente, 
                    EletronicoIndustrial, Registro,
                    Venda)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///banco.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True

CORS(app) 

db.init_app(app)

from app import routes
app.register_blueprint(routes.bp)

with app.app_context():
    db.create_all()