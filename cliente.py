
import api_cliente

# FUNÇÕES AUXILIARES

def pausar():
    input("\nPressione ENTER para continuar...")


def mostrar_dados(dados):
    """Exibe dados de forma organizada."""

    if isinstance(dados, list):
        if not dados:
            print("\nNenhum registro encontrado.")
            return

        for item in dados:
            print("-" * 50)
            for chave, valor in item.items():
                print(f"{chave}: {valor}")
        print("-" * 50)

    elif isinstance(dados, dict):
        print("-" * 50)
        for chave, valor in dados.items():
            print(f"{chave}: {valor}")
        print("-" * 50)

    else:
        print(dados)

# MENU DE PRODUTOS

def menu_produtos():

    while True:
        print("\n")
        print("-" * 20)
        print("PRODUTOS")
        print("-" * 20)
        print("1 - Listar produtos")
        print("2 - Buscar produto por ID")
        print("3 - Buscar produto por nome")
        print("4 - Cadastrar produto")
        print("5 - Alterar produto")
        print("6 - Excluir produto")
        print("0 - Voltar")
        print("-" * 20)

        opcao = input("Escolha uma opção: ")

        try:

            if opcao == "1":
                produtos = api_cliente.listar_produto()
                mostrar_dados(produtos)
                pausar()

            elif opcao == "2":
                id_produto = int(input("Digite o ID do produto: "))

                produto = api_cliente.obter_produto(id_produto)

                if produto is None:
                    print("\nProduto não encontrado.")
                else:
                    mostrar_dados(produto)

                pausar()

            elif opcao == "3":
                nome = input("Digite o nome do produto: ")

                produtos = api_cliente.buscar_produto(nome)

                mostrar_dados(produtos)

                pausar()

            elif opcao == "4":
                nome = input("Nome do produto: ")
                preco = int(input("Preço: "))
                qtd = int(input("Quantidade: "))

                produto = api_cliente.criar_produto(
                    nome,
                    preco,
                    qtd
                )

                print("\nProduto criado com sucesso!")
                mostrar_dados(produto)

                pausar()

            elif opcao == "5":
                id_produto = int(
                    input("ID do produto: ")
                )

                print("\nDeixe o campo vazio para não alterar.")

                nome = input("Novo nome: ")
                preco = input("Novo preço: ")
                qtd = input("Nova quantidade: ")

                dados = {}

                if nome:
                    dados["nome"] = nome

                if preco:
                    dados["preco"] = int(preco)

                if qtd:
                    dados["qtd"] = int(qtd)

                if not dados:
                    print("\nNenhum dado informado.")
                else:
                    produto = api_cliente.atualizar_produto(
                        id_produto,
                        dados
                    )

                    if produto is None:
                        print("\nProduto não encontrado.")
                    else:
                        print("\nProduto atualizado com sucesso!")
                        mostrar_dados(produto)

                pausar()

            elif opcao == "6":
                id_produto = int(
                    input("ID do produto: ")
                )

                confirmar = input(
                    "Tem certeza que deseja excluir? (s/n): "
                )

                if confirmar.lower() == "s":

                    excluido = api_cliente.excluir_produto(
                        id_produto
                    )

                    if excluido:
                        print(
                            "\nProduto excluído com sucesso!"
                        )
                    else:
                        print(
                            "\nProduto não encontrado."
                        )

                pausar()

            elif opcao == "0":
                break

            else:
                print("\nOpção inválida.")

        except ValueError:
            print("\nDigite um valor válido.")
            pausar()

        except Exception as e:
            print(f"\nErro: {e}")
            pausar()

# MENU DE ELETRÔNICOS

def menu_eletronicos():

    while True:
        print("\n")
        print("-" * 20)
        print("ELETRÔNICOS")
        print("-" * 20)
        print("1 - Listar eletrônicos")
        print("2 - Buscar eletrônico por ID")
        print("3 - Cadastrar eletrônico")
        print("4 - Alterar eletrônico")
        print("5 - Excluir eletrônico")
        print("0 - Voltar")
        print("-" * 20)

        opcao = input("Escolha uma opção: ")

        try:

            if opcao == "1":
                eletronicos = api_cliente.listar_eletronico()

                mostrar_dados(eletronicos)

                pausar()

            elif opcao == "2":
                id_eletronico = int(
                    input("ID do eletrônico: ")
                )

                eletronico = api_cliente.obter_eletronico(
                    id_eletronico
                )

                if eletronico is None:
                    print("\nEletrônico não encontrado.")
                else:
                    mostrar_dados(eletronico)

                pausar()

            elif opcao == "3":

                id_produto = int(
                    input("ID do produto: ")
                )

                marca = input("Marca: ")
                modelo = input("Modelo: ")

                print("\nSubtipo:")
                print("1 - Doméstico")
                print("2 - Industrial")
                print("3 - Inteligente")
                print("4 - Nenhum")

                subtipo_opcao = input(
                    "Escolha o subtipo: "
                )

                if subtipo_opcao == "1":

                    cor = input("Cor: ")
                    material = input("Material: ")

                    eletronico = api_cliente.criar_eletronico(
                        id_produto,
                        marca,
                        modelo,
                        "domestico",
                        cor=cor,
                        material=material
                    )

                elif subtipo_opcao == "2":

                    nicho = input("Nicho: ")
                    material = input("Material: ")

                    eletronico = api_cliente.criar_eletronico(
                        id_produto,
                        marca,
                        modelo,
                        "industrial",
                        nicho=nicho,
                        material=material
                    )

                elif subtipo_opcao == "3":

                    conectividade = input(
                        "Possui conectividade? (s/n): "
                    )

                    conectividade = (
                        conectividade.lower() == "s"
                    )

                    eletronico = api_cliente.criar_eletronico(
                        id_produto,
                        marca,
                        modelo,
                        "inteligente",
                        conectividade=conectividade
                    )

                elif subtipo_opcao == "4":

                    eletronico = api_cliente.criar_eletronico(
                        id_produto,
                        marca,
                        modelo
                    )

                else:
                    print("\nSubtipo inválido.")
                    pausar()
                    continue

                print(
                    "\nEletrônico criado com sucesso!"
                )

                mostrar_dados(eletronico)

                pausar()

            elif opcao == "4":

                id_eletronico = int(
                    input("ID do eletrônico: ")
                )

                print("\nCampos principais:")
                marca = input(
                    "Nova marca (ENTER para manter): "
                )

                modelo = input(
                    "Novo modelo (ENTER para manter): "
                )

                dados = {}

                if marca:
                    dados["marca"] = marca

                if modelo:
                    dados["modelo"] = modelo

                if not dados:
                    print("\nNenhum dado informado.")
                else:

                    eletronico = api_cliente.atualizar_eletronico(
                        id_eletronico,
                        dados
                    )

                    if eletronico is None:
                        print(
                            "\nEletrônico não encontrado."
                        )
                    else:
                        print(
                            "\nEletrônico atualizado com sucesso!"
                        )

                        mostrar_dados(eletronico)

                pausar()

            elif opcao == "5":

                id_eletronico = int(
                    input("ID do eletrônico: ")
                )

                confirmar = input(
                    "Tem certeza que deseja excluir? (s/n): "
                )

                if confirmar.lower() == "s":

                    excluido = api_cliente.excluir_eletronico(
                        id_eletronico
                    )

                    if excluido:
                        print(
                            "\nEletrônico excluído com sucesso!"
                        )
                    else:
                        print(
                            "\nEletrônico não encontrado."
                        )

                pausar()

            elif opcao == "0":
                break

            else:
                print("\nOpção inválida.")

        except ValueError:
            print("\nDigite um valor válido.")
            pausar()

        except Exception as e:
            print(f"\nErro: {e}")
            pausar()

# MENU DE VENDAS

def menu_vendas():

    while True:

        print("\n")
        print("-" * 20)
        print("VENDAS")
        print("-" * 20)
        print("1 - Listar vendas")
        print("2 - Buscar venda por ID")
        print("3 - Registrar venda")
        print("4 - Excluir venda")
        print("0 - Voltar")
        print("-" * 20)

        opcao = input("Escolha uma opção: ")

        try:

            if opcao == "1":

                vendas = api_cliente.listar_venda()

                mostrar_dados(vendas)

                pausar()

            elif opcao == "2":

                id_venda = int(
                    input("ID da venda: ")
                )

                venda = api_cliente.obter_venda(
                    id_venda
                )

                if venda is None:
                    print("\nVenda não encontrada.")
                else:
                    mostrar_dados(venda)

                pausar()

            elif opcao == "3":

                id_produto = int(
                    input("ID do produto: ")
                )

                quantidade = int(
                    input("Quantidade: ")
                )

                preco = int(
                    input("Preço unitário: ")
                )

                venda = api_cliente.criar_venda(
                    id_produto,
                    quantidade,
                    preco
                )

                print("\nVenda registrada com sucesso!")

                mostrar_dados(venda)

                pausar()

            elif opcao == "4":

                id_venda = int(
                    input("ID da venda: ")
                )

                confirmar = input(
                    "Tem certeza que deseja excluir? (s/n): "
                )

                if confirmar.lower() == "s":

                    excluido = api_cliente.excluir_venda(
                        id_venda
                    )

                    if excluido:
                        print(
                            "\nVenda excluída com sucesso!"
                        )
                    else:
                        print(
                            "\nVenda não encontrada."
                        )

                pausar()

            elif opcao == "0":
                break

            else:
                print("\nOpção inválida.")

        except ValueError:
            print("\nDigite um valor válido.")
            pausar()

        except Exception as e:
            print(f"\nErro: {e}")
            pausar()


# MENU DE REGISTROS


def menu_registros():

    while True:

        print("\n")
        print("-" * 20)
        print("REGISTROS")
        print("-" * 20)
        print("1 - Listar registros")
        print("2 - Filtrar por tipo de evento")
        print("3 - Filtrar por entidade")
        print("4 - Ordenar do mais antigo")
        print("5 - Ordenar do mais recente")
        print("6 - Buscar registro por ID")
        print("0 - Voltar")
        print("-" * 20)

        opcao = input("Escolha uma opção: ")

        try:

            if opcao == "1":

                registros = api_cliente.listar_registro()

                mostrar_dados(registros)

                pausar()

            elif opcao == "2":

                tipo = input(
                    "Tipo do evento (CRIACAO, ATUALIZACAO, "
                    "EXCLUSAO, VENDA, CANCELAMENTO): "
                )

                registros = api_cliente.listar_registro(
                    tipo_evento=tipo
                )

                mostrar_dados(registros)

                pausar()

            elif opcao == "3":

                entidade = input(
                    "Entidade (Produto, Eletronico, Venda): "
                )

                registros = api_cliente.listar_registro(
                    entidade=entidade
                )

                mostrar_dados(registros)

                pausar()

            elif opcao == "4":

                registros = api_cliente.listar_registro(
                    ordem="asc"
                )

                mostrar_dados(registros)

                pausar()

            elif opcao == "5":

                registros = api_cliente.listar_registro(
                    ordem="desc"
                )

                mostrar_dados(registros)

                pausar()

            elif opcao == "6":

                id_registro = int(
                    input("ID do registro: ")
                )

                registro = api_cliente.obter_registro(
                    id_registro
                )

                if registro is None:
                    print(
                        "\nRegistro não encontrado."
                    )
                else:
                    mostrar_dados(registro)

                pausar()

            elif opcao == "0":
                break

            else:
                print("\nOpção inválida.")

        except ValueError:
            print("\nDigite um valor válido.")
            pausar()

        except Exception as e:
            print(f"\nErro: {e}")
            pausar()


# MENU DE RELATÓRIOS


def menu_relatorios():

    while True:

        print("\n")
        print("-" * 20)
        print("RELATÓRIOS")
        print("-" * 20)
        print("1 - Faturamento total")
        print("2 - Produto mais vendido")
        print("3 - Vendas por produto")
        print("4 - Movimentações por tipo")
        print("0 - Voltar")
        print("-" * 20)

        opcao = input("Escolha uma opção: ")

        try:

            if opcao == "1":

                resultado = (
                    api_cliente.relatorio_faturamento()
                )

                mostrar_dados(resultado)

                pausar()

            elif opcao == "2":

                resultado = (
                    api_cliente.relatorio_produto_mais_vendido()
                )

                mostrar_dados(resultado)

                pausar()

            elif opcao == "3":

                resultado = (
                    api_cliente.relatorio_vendas_por_produto()
                )

                mostrar_dados(resultado)

                pausar()

            elif opcao == "4":

                resultado = (
                    api_cliente.relatorio_movimentacoes()
                )

                mostrar_dados(resultado)

                pausar()

            elif opcao == "0":
                break

            else:
                print("\nOpção inválida.")

        except Exception as e:
            print(f"\nErro: {e}")
            pausar()

# MENU PRINCIPAL

def menu_principal():

    while True:

        print("\n")
        print("SISTEMA DE GERENCIAMENTO")
        print("-" * 25)
        print("1 - Produtos")
        print("2 - Eletrônicos")
        print("3 - Vendas")
        print("4 - Registros")
        print("5 - Relatórios")
        print("0 - Sair")
        print("-" * 20)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_produtos()

        elif opcao == "2":
            menu_eletronicos()

        elif opcao == "3":
            menu_vendas()

        elif opcao == "4":
            menu_registros()

        elif opcao == "5":
            menu_relatorios()

        elif opcao == "0":
            print("\nEncerrando o sistema...")
            break

        else:
            print("\nOpção inválida. Tente novamente.")


# INÍCIO DO PROGRAMA

if __name__ == "__main__":

    try:
        resposta = api_cliente._executar(
            "GET",
            "/"
        )

        if resposta.status_code == 200:

            print("\n")
            print("CONEXÃO COM A API ESTABELECIDA")
            print("-" * 30)

            menu_principal()

        else:
            print(
                "\nA API respondeu com erro:",
                resposta.status_code
            )

    except Exception as e:
        print("\nNão foi possível iniciar o cliente.")
        print(f"Erro: {e}")

