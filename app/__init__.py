import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from app.models import (
    db, Produto, Eletronico,
    EletronicoDomestico, EletronicoInteligente,
    EletronicoIndustrial, Registro, Venda
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONT_DIR = os.path.join(BASE_DIR, "front")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///banco.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True

CORS(app)
db.init_app(app)

from app import routes
app.register_blueprint(routes.bp)

# Página do sistema
@app.route("/interface")
def interface():
    return send_from_directory(FRONT_DIR, "index.html")

# Arquivos CSS e JavaScript
@app.route("/front/<path:arquivo>")
def arquivos_front(arquivo):
    return send_from_directory(FRONT_DIR, arquivo)

with app.app_context():
    db.create_all()