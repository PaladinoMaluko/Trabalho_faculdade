from flask import request, jsonify
from app import app
from app.models import (
    db, Produto, Eletronico, EletronicoDomestico,
    EletronicoIndustrial, EletronicoInteligente, Registro, Venda
)

# dicionários


def produto_to_dict(p):
    return {
        "id": p.id,
        "nome": p.nome,
        "preco": p.preco,
        "qtd": p.qtd
    }


def eletronico_to_dict(e):
    return {
        "id": e.id,
        "id_produto": e.id_produto,
        "marca": e.marca,
        "modelo": e.modelo
    }


def eletronico_domestico_to_dict(ed):
    return {
        "id": ed.id,
        "id_eletronico": ed.id_eletronico,
        "cor": ed.cor,
        "material": ed.material
    }


def eletronico_industrial_to_dict(ei):
    return {
        "id": ei.id,
        "id_eletronico": ei.id_eletronico,
        "nicho": ei.nicho,
        "material": ei.material
    }


def eletronico_inteligente_to_dict(ei):
    return {
        "id": ei.id,
        "id_eletronico": ei.id_eletronico,
        "conectividade": ei.conectividade
    }


def venda_to_dict(v):
    return {
        "id": v.id,
        "id_produto": v.id_produto,
        "quantidade": v.quantidade,
        "preco_unitario": v.preco_unitario,
        "valor_total": v.valor_total,
        "data_venda": v.data_venda.isoformat() if v.data_venda else None
    }


def registro_to_dict(r):
    return {
        "id": r.id,
        "data_hora": r.data_hora.isoformat() if r.data_hora else None,
        "tipo_evento": r.tipo_evento,
        "entidade": r.entidade,
        "id_entidade": r.id_entidade,
        "descricao": r.descricao
    }


# rota inicial

@app.route('/')
@app.route('/index')
def index():
    return jsonify({"mensagem": "API funcionando"})


# produto

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([produto_to_dict(p) for p in produtos]), 200


@app.route('/produtos/<int:id>', methods=['GET'])
def obter_produto(id):
    produto = db.session.get(Produto, id)
    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify(produto_to_dict(produto)), 200


@app.route('/produtos', methods=['POST'])
def criar_produto():
    dados = request.get_json()

    if not dados or "nome" not in dados or "preco" not in dados:
        return jsonify({"erro": "Os campos 'nome' e 'preco' são obrigatórios"}), 400

    produto = Produto(
        nome=dados["nome"],
        preco=dados["preco"],
        qtd=dados.get("qtd", 0)
    )

    try:
        db.session.add(produto)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao criar produto: {e}"}), 500

    return jsonify(produto_to_dict(produto)), 201


@app.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    produto = db.session.get(Produto, id)
    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON não informado"}), 400

    for campo in ["nome", "preco", "qtd"]:
        if campo in dados:
            setattr(produto, campo, dados[campo])

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao atualizar produto: {e}"}), 500

    return jsonify(produto_to_dict(produto)), 200


@app.route('/produtos/<int:id>', methods=['DELETE'])
def excluir_produto(id):
    produto = db.session.get(Produto, id)
    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404

    try:
        db.session.delete(produto)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao excluir produto: {e}"}), 500

    return jsonify({"mensagem": "Produto excluído com sucesso"}), 200


# eletronico
@app.route('/eletronicos', methods=['GET'])
def listar_eletronicos():
    eletronicos = Eletronico.query.all()
    return jsonify([eletronico_to_dict(e) for e in eletronicos]), 200


@app.route('/eletronicos/<int:id>', methods=['GET'])
def obter_eletronico(id):
    eletronico = db.session.get(Eletronico, id)
    if eletronico is None:
        return jsonify({"erro": "Eletronico não encontrado"}), 404
    return jsonify(eletronico_to_dict(eletronico)), 200


@app.route('/eletronicos', methods=['POST'])
def criar_eletronico():
    dados = request.get_json()

    if not dados or "id_produto" not in dados or "marca" not in dados or "modelo" not in dados:
        return jsonify({"erro": "Os campos 'id_produto', 'marca' e 'modelo' são obrigatórios"}), 400

    produto = db.session.get(Produto, dados["id_produto"])
    if produto is None:
        return jsonify({"erro": "Produto informado não existe"}), 404

    eletronico = Eletronico(
        id_produto=dados["id_produto"],
        marca=dados["marca"],
        modelo=dados["modelo"]
    )

    try:
        db.session.add(eletronico)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao criar eletronico: {e}"}), 500

    return jsonify(eletronico_to_dict(eletronico)), 201


@app.route('/eletronicos/<int:id>', methods=['PUT'])
def atualizar_eletronico(id):
    eletronico = db.session.get(Eletronico, id)
    if eletronico is None:
        return jsonify({"erro": "Eletronico não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON não informado"}), 400

    for campo in ["marca", "modelo"]:
        if campo in dados:
            setattr(eletronico, campo, dados[campo])

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao atualizar eletronico: {e}"}), 500

    return jsonify(eletronico_to_dict(eletronico)), 200


@app.route('/eletronicos/<int:id>', methods=['DELETE'])
def excluir_eletronico(id):
    eletronico = db.session.get(Eletronico, id)
    if eletronico is None:
        return jsonify({"erro": "Eletronico não encontrado"}), 404

    try:
        db.session.delete(eletronico)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao excluir eletronico: {e}"}), 500

    return jsonify({"mensagem": "Eletronico excluído com sucesso"}), 200


# eletronico domestico

@app.route('/eletronicos-domesticos', methods=['GET'])
def listar_eletronicos_domesticos():
    itens = EletronicoDomestico.query.all()
    return jsonify([eletronico_domestico_to_dict(i) for i in itens]), 200


@app.route('/eletronicos-domesticos/<int:id>', methods=['GET'])
def obter_eletronico_domestico(id):
    item = db.session.get(EletronicoDomestico, id)
    if item is None:
        return jsonify({"erro": "Eletronico doméstico não encontrado"}), 404
    return jsonify(eletronico_domestico_to_dict(item)), 200


@app.route('/eletronicos-domesticos', methods=['POST'])
def criar_eletronico_domestico():
    dados = request.get_json()

    if not dados or "id_eletronico" not in dados:
        return jsonify({"erro": "O campo 'id_eletronico' é obrigatório"}), 400

    eletronico = db.session.get(Eletronico, dados["id_eletronico"])
    if eletronico is None:
        return jsonify({"erro": "Eletronico informado não existe"}), 404

    item = EletronicoDomestico(
        id_eletronico=dados["id_eletronico"],
        cor=dados.get("cor"),
        material=dados.get("material")
    )

    try:
        db.session.add(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao criar eletronico doméstico: {e}"}), 500

    return jsonify(eletronico_domestico_to_dict(item)), 201


@app.route('/eletronicos-domesticos/<int:id>', methods=['PUT'])
def atualizar_eletronico_domestico(id):
    item = db.session.get(EletronicoDomestico, id)
    if item is None:
        return jsonify({"erro": "Eletronico doméstico não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON não informado"}), 400

    for campo in ["cor", "material"]:
        if campo in dados:
            setattr(item, campo, dados[campo])

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao atualizar eletronico doméstico: {e}"}), 500

    return jsonify(eletronico_domestico_to_dict(item)), 200


@app.route('/eletronicos-domesticos/<int:id>', methods=['DELETE'])
def excluir_eletronico_domestico(id):
    item = db.session.get(EletronicoDomestico, id)
    if item is None:
        return jsonify({"erro": "Eletronico doméstico não encontrado"}), 404

    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao excluir eletronico doméstico: {e}"}), 500

    return jsonify({"mensagem": "Eletronico doméstico excluído com sucesso"}), 200


# eletronico industrial

@app.route('/eletronicos-industriais', methods=['GET'])
def listar_eletronicos_industriais():
    itens = EletronicoIndustrial.query.all()
    return jsonify([eletronico_industrial_to_dict(i) for i in itens]), 200


@app.route('/eletronicos-industriais/<int:id>', methods=['GET'])
def obter_eletronico_industrial(id):
    item = db.session.get(EletronicoIndustrial, id)
    if item is None:
        return jsonify({"erro": "Eletronico industrial não encontrado"}), 404
    return jsonify(eletronico_industrial_to_dict(item)), 200


@app.route('/eletronicos-industriais', methods=['POST'])
def criar_eletronico_industrial():
    dados = request.get_json()

    if not dados or "id_eletronico" not in dados:
        return jsonify({"erro": "O campo 'id_eletronico' é obrigatório"}), 400

    eletronico = db.session.get(Eletronico, dados["id_eletronico"])
    if eletronico is None:
        return jsonify({"erro": "Eletronico informado não existe"}), 404

    item = EletronicoIndustrial(
        id_eletronico=dados["id_eletronico"],
        nicho=dados.get("nicho"),
        material=dados.get("material")
    )

    try:
        db.session.add(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao criar eletronico industrial: {e}"}), 500

    return jsonify(eletronico_industrial_to_dict(item)), 201


@app.route('/eletronicos-industriais/<int:id>', methods=['PUT'])
def atualizar_eletronico_industrial(id):
    item = db.session.get(EletronicoIndustrial, id)
    if item is None:
        return jsonify({"erro": "Eletronico industrial não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON não informado"}), 400

    for campo in ["nicho", "material"]:
        if campo in dados:
            setattr(item, campo, dados[campo])

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao atualizar eletronico industrial: {e}"}), 500

    return jsonify(eletronico_industrial_to_dict(item)), 200


@app.route('/eletronicos-industriais/<int:id>', methods=['DELETE'])
def excluir_eletronico_industrial(id):
    item = db.session.get(EletronicoIndustrial, id)
    if item is None:
        return jsonify({"erro": "Eletronico industrial não encontrado"}), 404

    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao excluir eletronico industrial: {e}"}), 500

    return jsonify({"mensagem": "Eletronico industrial excluído com sucesso"}), 200


#eletronico inteligente

@app.route('/eletronicos-inteligentes', methods=['GET'])
def listar_eletronicos_inteligentes():
    itens = EletronicoInteligente.query.all()
    return jsonify([eletronico_inteligente_to_dict(i) for i in itens]), 200


@app.route('/eletronicos-inteligentes/<int:id>', methods=['GET'])
def obter_eletronico_inteligente(id):
    item = db.session.get(EletronicoInteligente, id)
    if item is None:
        return jsonify({"erro": "Eletronico inteligente não encontrado"}), 404
    return jsonify(eletronico_inteligente_to_dict(item)), 200


@app.route('/eletronicos-inteligentes', methods=['POST'])
def criar_eletronico_inteligente():
    dados = request.get_json()

    if not dados or "id_eletronico" not in dados:
        return jsonify({"erro": "O campo 'id_eletronico' é obrigatório"}), 400

    eletronico = db.session.get(Eletronico, dados["id_eletronico"])
    if eletronico is None:
        return jsonify({"erro": "Eletronico informado não existe"}), 404

    item = EletronicoInteligente(
        id_eletronico=dados["id_eletronico"],
        conectividade=dados.get("conectividade", False)
    )

    try:
        db.session.add(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao criar eletronico inteligente: {e}"}), 500

    return jsonify(eletronico_inteligente_to_dict(item)), 201


@app.route('/eletronicos-inteligentes/<int:id>', methods=['PUT'])
def atualizar_eletronico_inteligente(id):
    item = db.session.get(EletronicoInteligente, id)
    if item is None:
        return jsonify({"erro": "Eletronico inteligente não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON não informado"}), 400

    if "conectividade" in dados:
        item.conectividade = dados["conectividade"]

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao atualizar eletronico inteligente: {e}"}), 500

    return jsonify(eletronico_inteligente_to_dict(item)), 200


@app.route('/eletronicos-inteligentes/<int:id>', methods=['DELETE'])
def excluir_eletronico_inteligente(id):
    item = db.session.get(EletronicoInteligente, id)
    if item is None:
        return jsonify({"erro": "Eletronico inteligente não encontrado"}), 404

    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao excluir eletronico inteligente: {e}"}), 500

    return jsonify({"mensagem": "Eletronico inteligente excluído com sucesso"}), 200


# venda

@app.route('/vendas', methods=['GET'])
def listar_vendas():
    vendas = Venda.query.all()
    return jsonify([venda_to_dict(v) for v in vendas]), 200


@app.route('/vendas/<int:id>', methods=['GET'])
def obter_venda(id):
    venda = db.session.get(Venda, id)
    if venda is None:
        return jsonify({"erro": "Venda não encontrada"}), 404
    return jsonify(venda_to_dict(venda)), 200


@app.route('/vendas', methods=['POST'])
def criar_venda():
    dados = request.get_json()

    campos_obrigatorios = ["id_produto", "quantidade", "preco_unitario"]
    if not dados or not all(c in dados for c in campos_obrigatorios):
        return jsonify({"erro": "Os campos 'id_produto', 'quantidade' e 'preco_unitario' são obrigatórios"}), 400

    produto = db.session.get(Produto, dados["id_produto"])
    if produto is None:
        return jsonify({"erro": "Produto informado não existe"}), 404

    if dados["quantidade"] <= 0 or dados["preco_unitario"] <= 0:
        return jsonify({"erro": "Quantidade e preço unitário devem ser maiores que zero"}), 400

    venda = Venda(
        id_produto=dados["id_produto"],
        quantidade=dados["quantidade"],
        preco_unitario=dados["preco_unitario"],
        valor_total=dados["quantidade"] * dados["preco_unitario"]
    )

    try:
        db.session.add(venda)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao criar venda: {e}"}), 500

    return jsonify(venda_to_dict(venda)), 201


@app.route('/vendas/<int:id>', methods=['PUT'])
def atualizar_venda(id):
    venda = db.session.get(Venda, id)
    if venda is None:
        return jsonify({"erro": "Venda não encontrada"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON não informado"}), 400

    for campo in ["quantidade", "preco_unitario"]:
        if campo in dados:
            setattr(venda, campo, dados[campo])

    venda.valor_total = venda.quantidade * venda.preco_unitario

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao atualizar venda: {e}"}), 500

    return jsonify(venda_to_dict(venda)), 200


@app.route('/vendas/<int:id>', methods=['DELETE'])
def excluir_venda(id):
    venda = db.session.get(Venda, id)
    if venda is None:
        return jsonify({"erro": "Venda não encontrada"}), 404

    try:
        db.session.delete(venda)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao excluir venda: {e}"}), 500

    return jsonify({"mensagem": "Venda excluída com sucesso"}), 200



# registros

@app.route('/registros', methods=['GET'])
def listar_registros():
    registros = Registro.query.order_by(Registro.data_hora.desc()).all()
    return jsonify([registro_to_dict(r) for r in registros]), 200


@app.route('/registros/<int:id>', methods=['GET'])
def obter_registro(id):
    registro = db.session.get(Registro, id)
    if registro is None:
        return jsonify({"erro": "Registro não encontrado"}), 404
    return jsonify(registro_to_dict(registro)), 200


@app.route('/registros', methods=['POST'])
def criar_registro():
    dados = request.get_json()

    campos_obrigatorios = ["tipo_evento", "entidade", "id_entidade"]
    if not dados or not all(c in dados for c in campos_obrigatorios):
        return jsonify({"erro": "Os campos 'tipo_evento', 'entidade' e 'id_entidade' são obrigatórios"}), 400

    registro = Registro(
        tipo_evento=dados["tipo_evento"],
        entidade=dados["entidade"],
        id_entidade=dados["id_entidade"],
        descricao=dados.get("descricao")
    )

    try:
        db.session.add(registro)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao criar registro: {e}"}), 500

    return jsonify(registro_to_dict(registro)), 201


@app.route('/registros/<int:id>', methods=['PUT'])
def atualizar_registro(id):
    registro = db.session.get(Registro, id)
    if registro is None:
        return jsonify({"erro": "Registro não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON não informado"}), 400

    for campo in ["tipo_evento", "entidade", "id_entidade", "descricao"]:
        if campo in dados:
            setattr(registro, campo, dados[campo])

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao atualizar registro: {e}"}), 500

    return jsonify(registro_to_dict(registro)), 200


@app.route('/registros/<int:id>', methods=['DELETE'])
def excluir_registro(id):
    registro = db.session.get(Registro, id)
    if registro is None:
        return jsonify({"erro": "Registro não encontrado"}), 404

    try:
        db.session.delete(registro)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao excluir registro: {e}"}), 500

    return jsonify({"mensagem": "Registro excluído com sucesso"}), 200