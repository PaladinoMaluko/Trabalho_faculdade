from flask import Blueprint, jsonify, request
from app.models import db, Produto, Eletronico, EletronicoDomestico, EletronicoIndustrial, EletronicoInteligente, Venda, Registro

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

def buscar_eletronico_ou_erro(id):
    """
    Busca um eletronico pelo ID.
    Retorna (eletronico, None) se encontrar.
    Retorna (None, (json, status)) se não encontrar ou der erro.
    """
    try:
        eletronico = db.session.get(Eletronico, id)
    except Exception as e:
        print(f"Erro ao buscar eletronico: {e}")
        return None, (jsonify({"erro": "Erro interno"}), 500)

    if eletronico is None:
        return None, (jsonify({"erro": "Eletronico não encontrado"}), 404)

    return eletronico, None

def buscar_venda_ou_erro(id):
    """
    Busca uma venda pelo ID.
    Retorna (venda, None) se encontrar.
    Retorna (None, (json, status)) se não encontrar ou der erro.
    """
    try:
        venda = db.session.get(Venda, id)
    except Exception as e:
        print(f"Erro ao buscar venda: {e}")
        return None, (jsonify({"erro": "Erro interno"}), 500)

    if venda is None:
        return None, (jsonify({"erro": "Venda não encontrada"}), 404)

    return venda, None


@bp.route('/', methods=['GET'])
def index():
    return jsonify({"mensagem": "API funcionando"})


# ---- CRUD DE PRODUTO ----
@bp.route('/produtos', methods=['GET'])
def listar_produto():
    """Rota para listar todos os produtos"""
    try:
        produtos = Produto.query.all()

        return jsonify([produto.to_dict() for produto in produtos]), 200
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return jsonify({"erro": "Erro interno ao listar produtos"}), 500


@bp.route("/produtos/<int:id>", methods=["GET"])
def obter_produto(id):
    """Rota para obter um produto pelo ID"""
    produto, erro = buscar_produto_ou_erro(id)
    
    if erro:
        return erro

    return jsonify(produto.to_dict()), 200


@bp.route("/produtos/buscar", methods=["GET"])
def buscar_produto():
    """Rota para buscar produtos pelo nome"""
    nome = request.args.get("nome")

    if not nome:
        return jsonify({"erro": "O parâmetro 'nome' é obrigatório"}, 400)

    try:
        produtos = Produto.query.filter(Produto.nome.ilike(f"%{nome}%")).all()
        return jsonify([p.to_dict() for p in produtos]), 200
    except Exception as e:
        print(f"Erro ao buscar produtos: {e}")
        return jsonify({"erro": "Erro interno"}), 500


@bp.route("/produtos", methods=["POST"])
def criar_produto():
    """Rota para criar um novo produto"""
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "JSON não informado"}), 400

    if "nome" not in dados or "preco" not in dados:
        return jsonify({"erro": "Os campos 'nome' e 'preco' são obrigatórios"}), 400

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
        return jsonify({"erro": "Erro interno ao criar produto"}), 500

    return jsonify(produto.to_dict()), 201


@bp.route("/produtos/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    """Rota para atualizar um produto existente"""
    produto, erro = buscar_produto_ou_erro(id)

    if erro:
        return erro

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON não informado"}), 400

    try:
        campos_permitidos = ["nome", "preco", "qtd"]

        for campo in campos_permitidos:
            if campo in dados:
                setattr(produto, campo, dados[campo])

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao atualizar produto: {e}")
        return jsonify({"erro": "Erro interno ao atualizar produto"}), 500

    return jsonify(produto.to_dict()), 200


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
        return jsonify({"erro": "Erro interno ao deletar produto"}), 500
    

    return jsonify({"mensagem": "Produto excluído com sucesso"}), 200

# ---- CRUD DE ELETRONICO ----
@bp.route('/eletronicos', methods=['GET'])
def listar_eletronico():
    """Rota para listar todos os eletronicos"""
    try:
        eletronicos = Eletronico.query.all()

        return jsonify([eletronico.to_dict() for eletronico in eletronicos]), 200
    except Exception as e:
        print(f"Erro ao listar eletronicos: {e}")
        return jsonify({"erro": "Erro interno ao listar eletronicos"}), 500

@bp.route("/eletronicos/<int:id>", methods=["GET"])
def obter_eletronico(id):
    """Rota para obter um eletronico pelo ID"""
    eletronico, erro = buscar_eletronico_ou_erro(id)
    
    if erro:
        return erro

    return jsonify(eletronico.to_dict()), 200


@bp.route("/eletronicos", methods=["POST"])
def criar_eletronico():
    """Rota para criar um novo eletronico"""
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "JSON não informado"}, 400)

    if "id_produto" not in dados or "marca" not in dados or "modelo" not in dados:
        return jsonify({"erro": "Os campos são obrigatórios"}), 400

    # Verifica se existe um produto que seja um eletronico
    id_produto = dados["id_produto"]
    _, erro = buscar_produto_ou_erro(id_produto)
    if erro:
        return erro

    eletronico_existente = Eletronico.query.filter_by(id_produto=id_produto).first()
    if eletronico_existente:
        return jsonify({"erro": "Este produto já possui um eletrônico"}), 409
    
    eletronico = Eletronico(id_produto=id_produto, marca=dados["marca"], modelo=dados["modelo"])
    db.session.add(eletronico)
    # Evita fechar a transição 
    db.session.flush()

    # Criando o subtipo do eletronico
    subtipo = dados.get("subtipo")   

    if subtipo == "domestico":
        # criar EletronicoDomestico com cor e material
        domestico = EletronicoDomestico(id_eletronico=eletronico.id, cor=dados.get("cor"), material=dados.get("material"))
        db.session.add(domestico)

    elif subtipo == "industrial":
        # criar EletronicoIndustrial com nicho e material
        industrial = EletronicoIndustrial(id_eletronico=eletronico.id, nicho=dados.get("nicho"), material=dados.get("material"))
        db.session.add(industrial)

    elif subtipo == "inteligente":
        # criar EletronicoInteligente com conectividade
        inteligente = EletronicoInteligente(id_eletronico=eletronico.id, conectividade=dados.get("conectividade"))
        db.session.add(inteligente)

    elif subtipo is not None:
        # subtipo inválido
        db.session.rollback()
        return jsonify({"erro": "Subtipo inválido. Use 'domestico', 'industrial' ou 'inteligente'"}), 400

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar eletronico: {e}")
        return jsonify({"erro": "Erro interno ao criar eletronico"}), 500

    return jsonify(eletronico.to_dict()), 201


@bp.route("/eletronicos/<int:id>", methods=["PUT"])
def atualizar_eletronico(id):
    """Rota para atualizar um eletronico existente"""
    eletronico, erro = buscar_eletronico_ou_erro(id)

    if erro:
        return erro

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON não informado"}), 400

    subtipo_novo = dados.get("subtipo") if "subtipo" in dados else None
    tem_campo_subtipo = "subtipo" in dados

    try:
        campos_permitidos = ["marca", "modelo"]

        for campo in campos_permitidos:
            if campo in dados:
                setattr(eletronico, campo, dados[campo])

        if not tem_campo_subtipo:
            # cliente não mandou "subtipo" -> não mexe
            pass

        elif subtipo_novo is None:
            # cliente mandou "subtipo": null -> remove o subtipo atual
            if eletronico.eletronicodomestico:
                db.session.delete(eletronico.eletronicodomestico)
            elif eletronico.eletronicoindustrial:
                db.session.delete(eletronico.eletronicoindustrial)
            elif eletronico.eletronicointeligente:
                db.session.delete(eletronico.eletronicointeligente)

        elif subtipo_novo == "domestico":
            if eletronico.eletronicodomestico:
                # já é doméstico -> atualiza os campos
                for campo in ["cor", "material"]:
                    if campo in dados:
                        setattr(eletronico.eletronicodomestico, campo, dados[campo])
            elif eletronico.eletronicoindustrial or eletronico.eletronicointeligente:
                # já tem outro subtipo -> erro
                db.session.rollback()
                return jsonify({"erro": "Não é possível trocar o subtipo. Remova o subtipo atual primeiro."}), 400
            else:
                # é genérico -> cria o subtipo
                domestico = EletronicoDomestico(
                    id_eletronico=eletronico.id,
                    cor=dados.get("cor"),
                    material=dados.get("material")
                )
                db.session.add(domestico)

        elif subtipo_novo == "industrial":
            if eletronico.eletronicoindustrial:
                # já é industrial -> atualiza os campos
                for campo in ["nicho", "material"]:
                    if campo in dados:
                        setattr(eletronico.eletronicoindustrial, campo, dados[campo])
            elif eletronico.eletronicodomestico or eletronico.eletronicointeligente:
                # já tem outro subtipo -> erro
                db.session.rollback()
                return jsonify({"erro": "Não é possível trocar o subtipo. Remova o subtipo atual primeiro."}), 400
            else:
                # é genérico -> cria o subtipo
                industrial = EletronicoIndustrial(
                    id_eletronico=eletronico.id,
                    nicho=dados.get("nicho"),
                    material=dados.get("material")
                )
                db.session.add(industrial)
            
        elif subtipo_novo == "inteligente":
            if eletronico.eletronicointeligente:
                # já é inteligente -> atualiza os campos
                for campo in ["conectividade"]:
                    if campo in dados:
                        setattr(eletronico.eletronicointeligente, campo, dados[campo])
            elif eletronico.eletronicoindustrial or eletronico.eletronicodomestico:
                # já tem outro subtipo -> erro
                db.session.rollback()
                return jsonify({"erro": "Não é possível trocar o subtipo. Remova o subtipo atual primeiro."}), 400
            else:
                # é genérico -> cria o subtipo
                inteligente = EletronicoInteligente(
                    id_eletronico=eletronico.id,
                    conectividade=dados.get("conectividade")
                )
                db.session.add(inteligente)
        else:
            # subtipo inválido (string diferente das três válidas)
            db.session.rollback()
            return jsonify({"erro": "Subtipo inválido. Use 'domestico', 'industrial' ou 'inteligente'"}), 400

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao atualizar eletronico: {e}")
        return jsonify({"erro": "Erro interno ao atualizar eletronico"}), 500

    return jsonify(eletronico.to_dict()), 200


@bp.route("/eletronicos/<int:id>", methods=["DELETE"])
def excluir_eletronico(id):
    """Rota para excluir um eletronico existente"""
    eletronico, erro = buscar_eletronico_ou_erro(id)
        
    if erro:
        return erro

    try:
        # Deletanto subtipo do eletronico primeiro
        if eletronico.eletronicodomestico:
            db.session.delete(eletronico.eletronicodomestico)
        elif eletronico.eletronicoindustrial:
            db.session.delete(eletronico.eletronicoindustrial)
        elif eletronico.eletronicointeligente:
            db.session.delete(eletronico.eletronicointeligente)

        db.session.delete(eletronico)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao deletar eletronico: {e}")
        return jsonify({"erro": "Erro interno ao deletar eletronico"}), 500
    

    return jsonify({"mensagem": "Eletronico excluído com sucesso"}), 200


# ---- ROTAS DE ACESSO DE VENDAS ----
@bp.route('/vendas', methods=['GET'])
def listar_venda():
    """Rota para listar todas as vendas"""
    try:
        vendas = Venda.query.all()

        return jsonify([venda.to_dict() for venda in vendas]), 200
    except Exception as e:
        print(f"Erro ao listar vendas: {e}")
        return jsonify({"erro": "Erro interno ao listar vendas"}), 500


@bp.route("/vendas/<int:id>", methods=["GET"])
def obter_venda(id):
    """Rota para obter uma venda pelo ID"""
    venda, erro = buscar_venda_ou_erro(id)
    
    if erro:
        return erro

    return jsonify(venda.to_dict()), 200


@bp.route("/vendas", methods=["POST"])
def criar_venda():
    """Rota para criar uma nova venda"""
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "JSON não informado"}, 400)

    if "id_produto" not in dados or "quantidade" not in dados or "preco_unitario" not in dados:
        return jsonify({"erro": "Os campos são obrigatórios"}), 400

    # Verifica se existe um produto 
    id_produto = dados["id_produto"]
    produto, erro = buscar_produto_ou_erro(id_produto)
    if erro:
        return erro
    
    if dados["quantidade"] <= 0 or dados["preco_unitario"] <= 0:
        return jsonify({"erro": "Quantidade e preço devem ser maiores que zero"}), 400

    venda = Venda(id_produto=id_produto, quantidade=dados["quantidade"], preco_unitario=dados["preco_unitario"], valor_total=dados["quantidade"] * dados["preco_unitario"])

    try:
        db.session.add(venda)
        db.session.flush()   

        registro = Registro(
            tipo_evento="VENDA",
            entidade="Venda",
            id_entidade=venda.id,
            descricao=f"Venda de {dados['quantidade']}x {produto.nome} por R$ {venda.valor_total}"
        )

        db.session.add(registro)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar venda: {e}")
        return jsonify({"erro": "Erro interno ao criar venda"}), 500

    return jsonify(venda.to_dict()), 201

@bp.route("/vendas/<int:id>", methods=["DELETE"])
def excluir_venda(id):
    """Rota para excluir uma venda existente"""
    venda, erro = buscar_venda_ou_erro(id)
        
    if erro:
        return erro

    try:
        db.session.delete(venda)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao deletar venda: {e}")
        return jsonify({"erro": "Erro interno ao deletar venda"}), 500
    

    return jsonify({"mensagem": "Venda excluída com sucesso"}), 200