import requests

# A ponta para o servidor que esta rodando
BASE_URL = "http://127.0.0.1:5000"

# Funções auxiliares
def _executar(metodo, endpoint, json_body=None):
    """Faz a requisição HTTP. Trata apenas erro de conexão."""
    try:
        # Se for enviado um json (corpo da requisição)
        if json_body is not None:
            return requests.request(metodo, f"{BASE_URL}{endpoint}", json=json_body)
        
        return requests.request(metodo, f"{BASE_URL}{endpoint}")
    except requests.exceptions.ConnectionError:
        raise Exception("Não foi possível conectar à API. Ela está rodando?")


def _lancar_erro(response):
    """Extrai a mensagem de erro da resposta e lança exceção."""
    try:
        mensagem = response.json().get("erro", "Erro desconhecido")
    except Exception:
        mensagem = "Erro desconhecido"
    raise Exception(f"Erro {response.status_code}: {mensagem}")


def _requisicao(metodo, endpoint, json_body=None, status_sucesso=200, aceitar_404=False):
    """
    Faz requisição e exige sucesso. Aceita o argumenta 'aceitar_404' para tratar
    erros 404
    """
    
    response = _executar(metodo, endpoint, json_body)

    if response.status_code == status_sucesso:
        return response.json()

    if aceitar_404 and response.status_code == 404:
        return None

    _lancar_erro(response)


# --- PRODUTO ---
def listar_produto():
    """Faz GET para produtos e retorna uma lista"""
    return _requisicao("GET", "/produtos")
            
def obter_produto(id):
    """Faz GET para produto usando seu ID como referencia"""
    return _requisicao("GET", f"/produtos/{id}", aceitar_404=True) 

def buscar_produto(nome):
    """Faz GET para produto usando seu NOME como referencia"""
    return _requisicao("GET", f"/produtos/buscar?nome={nome}", aceitar_404=True)

def criar_produto(nome, preco, qtd):
    """Faz POST para produto criando ele no banco"""
    return _requisicao(
        "POST",
        "/produtos",
        json_body={"nome": nome, "preco": preco, "qtd": qtd},
        status_sucesso=201
    )

def atualizar_produto(id, dados):
    """Faz PUT para produto onde `dados` é um dicionário com os campos a atualizar"""
    return _requisicao("PUT", f"/produtos/{id}", json_body=dados, aceitar_404=True)

def excluir_produto(id):
    """Faz DELETE para produto que retorna True se excluído, False se não encontrado"""
    resultado = _requisicao("DELETE", f"/produtos/{id}", aceitar_404=True)
    return resultado is not None


# --- ELETRONICOS ---
def listar_eletronico():
    """Faz GET para eletronico e retorna uma lista"""
    return _requisicao("GET", "/eletronicos")
            
def obter_eletronico(id):
    """Faz GET para eletronico usando seu ID como referencia"""
    return _requisicao("GET", f"/eletronicos/{id}", aceitar_404=True) 

def criar_eletronico(id_produto, marca, modelo, subtipo=None, **extras):
    """
    Faz POST para eletronico criando ele no banco. Se `subtipo` for informado, envia os campos extras
    (cor/material, nicho, conectividade) junto no JSON.
    """
    body = {
        "id_produto": id_produto,
        "marca": marca,
        "modelo": modelo
    }
    if subtipo:
        body["subtipo"] = subtipo
        body.update(extras)  # adiciona cor, material, nicho, conectividade...

    return _requisicao("POST", "/eletronicos", json_body=body, status_sucesso=201)

def atualizar_eletronico(id, dados):
    """Faz PUT para eletronico onde `dados` é um dicionário com os campos a atualizar COMPLETO(inclua subtipos)"""
    return _requisicao("PUT", f"/eletronicos/{id}", json_body=dados, aceitar_404=True)

def excluir_eletronico(id):
    """Faz DELETE para eletronico que retorna True se excluído, False se não encontrado"""
    resultado = _requisicao("DELETE", f"/eletronicos/{id}", aceitar_404=True)
    return resultado is not None

# --- VENDA ---
def listar_venda():
    """Faz GET para venda e retorna uma lista"""
    return _requisicao("GET", "/vendas")

def obter_venda(id):
    """Faz GET para venda usando seu ID como referencia"""
    return _requisicao("GET", f"/vendas/{id}", aceitar_404=True)

def criar_venda(id_produto, quantidade, preco_unitario):
    """Faz POST para venda criando-a no banco"""
    return _requisicao(
        "POST", "/vendas",
        json_body={"id_produto": id_produto, "quantidade": quantidade, "preco_unitario": preco_unitario},
        status_sucesso=201
    )

def excluir_venda(id):
    """Faz DELETE para venda que retorna True se excluída, False se não encontrada"""
    resultado = _requisicao("DELETE", f"/vendas/{id}", aceitar_404=True)
    return resultado is not None


# --- REGISTRO ---
def listar_registro(tipo_evento=None, entidade=None, ordem=None):
    """Faz GET para registro e o retorna uma lista com filtro opicionais"""
    params = []
    if tipo_evento: params.append(f"tipo_evento={tipo_evento}")
    if entidade:    params.append(f"entidade={entidade}")
    if ordem:       params.append(f"ordem={ordem}")
    url = "/registros"
    if params:
        url += "?" + "&".join(params)
    return _requisicao("GET", url)

def obter_registro(id):
    """Faz GET para registro usando seu ID como referencia"""
    return _requisicao("GET", f"/registros/{id}", aceitar_404=True)


# --- RELATÓRIOS ---
def relatorio_faturamento():
    """Retorna o faturamento total"""
    return _requisicao("GET", "/relatorios/faturamento-total")

def relatorio_produto_mais_vendido():
    """Retorna o produto mais vendido"""
    return _requisicao("GET", "/relatorios/produto-mais-vendido")

def relatorio_vendas_por_produto():
    """Retorna vendas por cada produto"""
    return _requisicao("GET", "/relatorios/vendas-por-produto")

def relatorio_movimentacoes():
    """Retorna movimentações por cada tipo"""
    return _requisicao("GET", "/relatorios/movimentacoes-por-tipo")

if __name__ == "__main__":
    pass