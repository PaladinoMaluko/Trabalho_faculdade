from flask import Blueprint, jsonify
from app.models import db, Produto

bp = Blueprint('api', __name__)

@bp.route('/', methods=['GET'])
def index():
    return jsonify({"mensagem": "API funcionando"})

@bp.route('/produtos', methods=['GET'])
def listar_produtos():
    """Rota para listar todos os produtos"""
    try:
        produtos = Produto.query.all()

        return jsonify([
            produto.to_dict()
            for produto in produtos
        ], 200)
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return jsonify({"erro": "Erro interno ao listar produtos"}, 500)



@bp.route("/produtos/<int:id>", methods=["GET"])
def obter_produto(id):
    """Rota para obter um produto pelo ID"""

    try:
        produto = db.session.get(Produto, id)
    except Exception as e:
        print(f"Erro ao buscar produto: {e}")
        return jsonify({"erro": "Erro interno"}), 500

    if produto is not None:
        return jsonify(produto.to_dict())

    return jsonify({"erro": "Produto não encontrado"}), 404
       
       