from flask import Blueprint, jsonify, request
from app.models import db, Produto

bp = Blueprint('api', __name__)

# funções auxiliares
def buscar_produto_ou_erro(id):
    """
    Busca um produto pelo ID.
    Retorna (produto, None) se encontrar.
    Retorna (None, (json, status)) se não encontrar ou der erro.
    """
    try:
        produto = db.session.get(Produto, id)
    except Exception as e:
        print(f"Erro ao buscar produto: {e}")
        return None, (jsonify({"erro": "Erro interno"}), 500)

    if produto is None:
        return None, (jsonify({"erro": "Produto não encontrado"}), 404)

    return produto, None


@bp.route('/', methods=['GET'])
def index():
    return jsonify({"mensagem": "API funcionando"})

@bp.route('/produtos', methods=['GET'])
def listar_produtos():
    """Rota para listar todos os produtos"""
    try:
        produtos = Produto.query.all()

        return jsonify([produto.to_dict() for produto in produtos], 200)
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return jsonify({"erro": "Erro interno ao listar produtos"}, 500)


@bp.route("/produtos/<int:id>", methods=["GET"])
def obter_produto(id):
    """Rota para obter um produto pelo ID"""
    produto, erro = buscar_produto_ou_erro(id)
    
    if erro:
        return erro

    return jsonify(produto.to_dict(), 200)


@bp.route("/produtos/buscar", methods=["GET"])
def buscar_produtos():
    """Rota para buscar produtos pelo nome"""
    nome = request.args.get("nome")

    if not nome:
        return jsonify({"erro": "O parâmetro 'nome' é obrigatório"}, 400)

    try:
        produtos = Produto.query.filter(Produto.nome.ilike(f"%{nome}%")).all()
        return jsonify([p.to_dict() for p in produtos]), 200
    except Exception as e:
        print(f"Erro ao buscar produtos: {e}")
        return jsonify({"erro": "Erro interno"}, 500)


@bp.route("/produtos", methods=["POST"])
def criar_produto():
    """Rota para criar um novo produto"""
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "JSON não informado"}, 400)

    if "nome" not in dados or "preco" not in dados:
        return jsonify({"erro": "Os campos 'nome' e 'preco' são obrigatórios"}, 400)

    # Verifica se já existe um produto com o mesmo nome
    produto_existente = Produto.query.filter_by(nome=dados["nome"]).first()

    if produto_existente:
        return jsonify({
                "erro": "Já existe um produto com esse nome",
                "produto_existente": produto_existente.to_dict()
            }), 409

    produto = Produto(nome=dados["nome"], preco=dados["preco"], qtd=dados.get("qtd",0))

    try:
        db.session.add(produto)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar produto: {e}")
        return jsonify({"erro": "Erro interno ao criar produto"}, 500)

    return jsonify(produto.to_dict(), 201)


@bp.route("/produtos/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    """Rota para atualizar um produto existente"""
    produto, erro = buscar_produto_ou_erro(id)

    if erro:
        return erro

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON não informado"}, 400)

    try:
        campos_permitidos = ["nome", "preco", "qtd"]

        for campo in campos_permitidos:
            if campo in dados:
                setattr(produto, campo, dados[campo])

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao atualizar produto: {e}")
        return jsonify({"erro": "Erro interno ao atualizar produto"}, 500)

    return jsonify(produto.to_dict(), 200)


@bp.route("/produtos/<int:id>", methods=["DELETE"])
def excluir_produto(id):
    """Rota para excluir um produto existente"""
    produto, erro = buscar_produto_ou_erro(id)
        
    if erro:
        return erro

    try:
        db.session.delete(produto)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao deletar produto: {e}")
        return jsonify({"erro": "Erro interno ao deletar produto"}, 500)
    

    return jsonify({"mensagem": "Produto excluído com sucesso"}, 200)
