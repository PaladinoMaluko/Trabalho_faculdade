import unittest
import requests
import time

BASE_URL = "http://127.0.0.1:5000"


class TestAPI(unittest.TestCase):

    produto_id = None
    eletronico_id = None
    venda_id = None

    nome_produto = f"TESTE Produto {int(time.time())}"

    @classmethod
    def setUpClass(cls):
        """
        Verifica se a API está funcionando antes de iniciar os testes.
        """
        try:
            response = requests.get(f"{BASE_URL}/", timeout=5)
        except requests.exceptions.ConnectionError:
            raise Exception(
                "\nAPI não está rodando.\n"
                "Abra outro terminal e execute:\n"
                "python3 run.py\n"
            )

        if response.status_code != 200:
            raise Exception(
                f"API respondeu com status {response.status_code}"
            )

        print("        TESTES DA API")
        print("   ")

  
    # PRODUTO
    

    def test_01_api_funcionando(self):
        response = requests.get(f"{BASE_URL}/")

        self.assertEqual(response.status_code, 200)

        dados = response.json()

        self.assertIn("mensagem", dados)
        self.assertEqual(dados["mensagem"], "API funcionando")

        print("[OK] API está funcionando")

    def test_02_criar_produto(self):
        dados = {
            "nome": self.nome_produto,
            "preco": 100,
            "qtd": 10
        }

        response = requests.post(
            f"{BASE_URL}/produtos",
            json=dados
        )

        self.assertEqual(response.status_code, 201)

        produto = response.json()

        self.assertIn("id", produto)
        self.assertEqual(produto["nome"], self.nome_produto)
        self.assertEqual(produto["preco"], 100)
        self.assertEqual(produto["qtd"], 10)

        TestAPI.produto_id = produto["id"]

        print("[OK] Criar produto")

    def test_03_listar_produtos(self):
        response = requests.get(f"{BASE_URL}/produtos")

        self.assertEqual(response.status_code, 200)

        produtos = response.json()

        self.assertIsInstance(produtos, list)

        encontrado = any(
            produto["id"] == TestAPI.produto_id
            for produto in produtos
        )

        self.assertTrue(encontrado)

        print("[OK] Listar produtos")

    def test_04_obter_produto(self):
        response = requests.get(
            f"{BASE_URL}/produtos/{TestAPI.produto_id}"
        )

        self.assertEqual(response.status_code, 200)

        produto = response.json()

        self.assertEqual(
            produto["id"],
            TestAPI.produto_id
        )

        print("[OK] Buscar produto por ID")

    def test_05_buscar_produto_nome(self):
        response = requests.get(
            f"{BASE_URL}/produtos/buscar",
            params={"nome": self.nome_produto}
        )

        self.assertEqual(response.status_code, 200)

        produtos = response.json()

        self.assertIsInstance(produtos, list)
        self.assertGreaterEqual(len(produtos), 1)

        print("[OK] Buscar produto por nome")

    def test_06_atualizar_produto(self):
        dados = {
            "preco": 150,
            "qtd": 20
        }

        response = requests.put(
            f"{BASE_URL}/produtos/{TestAPI.produto_id}",
            json=dados
        )

        self.assertEqual(response.status_code, 200)

        produto = response.json()

        self.assertEqual(produto["preco"], 150)
        self.assertEqual(produto["qtd"], 20)

        print("[OK] Atualizar produto")

    # ELETRÔNICO

    def test_07_criar_eletronico(self):
        dados = {
            "id_produto": TestAPI.produto_id,
            "marca": "TESTE",
            "modelo": "Notebook Teste",
            "subtipo": "inteligente",
            "conectividade": True
        }

        response = requests.post(
            f"{BASE_URL}/eletronicos",
            json=dados
        )

        self.assertEqual(response.status_code, 201)

        eletronico = response.json()

        self.assertIn("id", eletronico)
        self.assertEqual(
            eletronico["id_produto"],
            TestAPI.produto_id
        )
        self.assertEqual(
            eletronico["marca"],
            "TESTE"
        )
        self.assertEqual(
            eletronico["modelo"],
            "Notebook Teste"
        )

        TestAPI.eletronico_id = eletronico["id"]

        print("[OK] Criar eletrônico")

    def test_08_listar_eletronicos(self):
        response = requests.get(
            f"{BASE_URL}/eletronicos"
        )

        self.assertEqual(response.status_code, 200)

        eletronicos = response.json()

        self.assertIsInstance(eletronicos, list)

        encontrado = any(
            item["id"] == TestAPI.eletronico_id
            for item in eletronicos
        )

        self.assertTrue(encontrado)

        print("[OK] Listar eletrônicos")

    def test_09_obter_eletronico(self):
        response = requests.get(
            f"{BASE_URL}/eletronicos/{TestAPI.eletronico_id}"
        )

        self.assertEqual(response.status_code, 200)

        eletronico = response.json()

        self.assertEqual(
            eletronico["id"],
            TestAPI.eletronico_id
        )

        self.assertIsNotNone(
            eletronico["eletronicointeligente"]
        )

        print("[OK] Buscar eletrônico")

    def test_10_atualizar_eletronico(self):
        dados = {
            "marca": "TESTE ATUALIZADO",
            "modelo": "Notebook Atualizado"
        }

        response = requests.put(
            f"{BASE_URL}/eletronicos/{TestAPI.eletronico_id}",
            json=dados
        )

        self.assertEqual(response.status_code, 200)

        eletronico = response.json()

        self.assertEqual(
            eletronico["marca"],
            "TESTE ATUALIZADO"
        )

        self.assertEqual(
            eletronico["modelo"],
            "Notebook Atualizado"
        )

        print("[OK] Atualizar eletrônico")

    # TESTES DOS SUBTIPOS DE ELETRÔNICO

    def test_26_criar_eletronico_domestico(self):
        # Cria outro produto para testar o subtipo doméstico
        dados_produto = {
            "nome": f"TESTE Domestico {int(time.time())}",
            "preco": 200,
            "qtd": 5
        }

        response_produto = requests.post(
            f"{BASE_URL}/produtos",
            json=dados_produto
        )

        self.assertEqual(response_produto.status_code, 201)

        produto = response_produto.json()
        produto_id = produto["id"]

        dados_eletronico = {
            "id_produto": produto_id,
            "marca": "TESTE",
            "modelo": "Geladeira Teste",
            "subtipo": "domestico",
            "cor": "Branca",
            "material": "Inox"
        }

        response = requests.post(
            f"{BASE_URL}/eletronicos",
            json=dados_eletronico
        )

        self.assertEqual(response.status_code, 201)

        eletronico = response.json()

        self.assertIsNotNone(
            eletronico["eletronicodomestico"]
        )

        self.assertEqual(
            eletronico["eletronicodomestico"]["cor"],
            "Branca"
        )

        self.assertEqual(
            eletronico["eletronicodomestico"]["material"],
            "Inox"
        )

        # Limpeza
        eletronico_id = eletronico["id"]

        requests.delete(
            f"{BASE_URL}/eletronicos/{eletronico_id}"
        )

        requests.delete(
            f"{BASE_URL}/produtos/{produto_id}"
        )

        print("[OK] Criar eletrônico doméstico")


    def test_27_criar_eletronico_industrial(self):
        # Cria outro produto para testar o subtipo industrial
        dados_produto = {
            "nome": f"TESTE Industrial {int(time.time())}",
            "preco": 300,
            "qtd": 5
        }

        response_produto = requests.post(
            f"{BASE_URL}/produtos",
            json=dados_produto
        )

        self.assertEqual(response_produto.status_code, 201)

        produto = response_produto.json()
        produto_id = produto["id"]

        dados_eletronico = {
            "id_produto": produto_id,
            "marca": "TESTE",
            "modelo": "Maquina Teste",
            "subtipo": "industrial",
            "nicho": "Industria",
            "material": "Metal"
        }

        response = requests.post(
            f"{BASE_URL}/eletronicos",
            json=dados_eletronico
        )

        self.assertEqual(response.status_code, 201)

        eletronico = response.json()

        self.assertIsNotNone(
            eletronico["eletronicoindustrial"]
        )

        self.assertEqual(
            eletronico["eletronicoindustrial"]["nicho"],
            "Industria"
        )

        self.assertEqual(
            eletronico["eletronicoindustrial"]["material"],
            "Metal"
        )

        # Limpeza
        eletronico_id = eletronico["id"]

        requests.delete(
            f"{BASE_URL}/eletronicos/{eletronico_id}"
        )

        requests.delete(
            f"{BASE_URL}/produtos/{produto_id}"
        )

        print("[OK] Criar eletrônico industrial")


    def test_28_subtipo_invalido(self):
        # Cria um produto para testar o erro
        dados_produto = {
            "nome": f"TESTE Subtipo Invalido {int(time.time())}",
            "preco": 400,
            "qtd": 5
        }

        response_produto = requests.post(
            f"{BASE_URL}/produtos",
            json=dados_produto
        )

        self.assertEqual(response_produto.status_code, 201)

        produto = response_produto.json()
        produto_id = produto["id"]

        dados_eletronico = {
            "id_produto": produto_id,
            "marca": "TESTE",
            "modelo": "Produto Teste",
            "subtipo": "subtipo_invalido"
        }

        response = requests.post(
            f"{BASE_URL}/eletronicos",
            json=dados_eletronico
        )

        self.assertEqual(response.status_code, 400)

        dados = response.json()

        self.assertIn("erro", dados)

        # Como o subtipo é inválido, o eletrônico não deve
        # permanecer no banco. Removemos apenas o produto.
        requests.delete(
            f"{BASE_URL}/produtos/{produto_id}"
        )

        print("[OK] Subtipo inválido → 400")

    # VENDA

    def test_11_criar_venda(self):
        dados = {
            "id_produto": TestAPI.produto_id,
            "quantidade": 2,
            "preco_unitario": 150
        }

        response = requests.post(
            f"{BASE_URL}/vendas",
            json=dados
        )

        self.assertEqual(response.status_code, 201)

        venda = response.json()

        self.assertIn("id", venda)

        self.assertEqual(
            venda["id_produto"],
            TestAPI.produto_id
        )

        self.assertEqual(
            venda["quantidade"],
            2
        )

        self.assertEqual(
            venda["preco_unitario"],
            150
        )

        self.assertEqual(
            venda["valor_total"],
            300
        )

        TestAPI.venda_id = venda["id"]

        print("[OK] Criar venda")

    def test_12_listar_vendas(self):
        response = requests.get(
            f"{BASE_URL}/vendas"
        )

        self.assertEqual(response.status_code, 200)

        vendas = response.json()

        self.assertIsInstance(vendas, list)

        encontrado = any(
            venda["id"] == TestAPI.venda_id
            for venda in vendas
        )

        self.assertTrue(encontrado)

        print("[OK] Listar vendas")

    def test_13_obter_venda(self):
        response = requests.get(
            f"{BASE_URL}/vendas/{TestAPI.venda_id}"
        )

        self.assertEqual(response.status_code, 200)

        venda = response.json()

        self.assertEqual(
            venda["id"],
            TestAPI.venda_id
        )

        print("[OK] Buscar venda")

    # REGISTROS

    def test_14_listar_registros(self):
        response = requests.get(
            f"{BASE_URL}/registros"
        )

        self.assertEqual(response.status_code, 200)

        registros = response.json()

        self.assertIsInstance(registros, list)

        self.assertGreaterEqual(
            len(registros),
            1
        )

        print("[OK] Listar registros")

    def test_15_filtrar_registros(self):
        response = requests.get(
            f"{BASE_URL}/registros",
            params={
                "tipo_evento": "CRIACAO"
            }
        )

        self.assertEqual(response.status_code, 200)

        registros = response.json()

        self.assertIsInstance(registros, list)

        for registro in registros:
            self.assertEqual(
                registro["tipo_evento"],
                "CRIACAO"
            )

        print("[OK] Filtrar registros")

    # RELATÓRIOS

    def test_16_relatorio_faturamento(self):
        response = requests.get(
            f"{BASE_URL}/relatorios/faturamento-total"
        )

        self.assertEqual(response.status_code, 200)

        dados = response.json()

        self.assertIn(
            "faturamento_total",
            dados
        )

        self.assertGreaterEqual(
            dados["faturamento_total"],
            0
        )

        print("[OK] Relatório de faturamento")

    def test_17_relatorio_produto_mais_vendido(self):
        response = requests.get(
            f"{BASE_URL}/relatorios/produto-mais-vendido"
        )

        self.assertEqual(response.status_code, 200)

        dados = response.json()

        self.assertTrue(
            "id" in dados
            or "mensagem" in dados
        )

        print("[OK] Relatório de produto mais vendido")

    def test_18_relatorio_vendas_por_produto(self):
        response = requests.get(
            f"{BASE_URL}/relatorios/vendas-por-produto"
        )

        self.assertEqual(response.status_code, 200)

        dados = response.json()

        self.assertIsInstance(
            dados,
            list
        )

        print("[OK] Relatório de vendas por produto")

    def test_19_relatorio_movimentacoes(self):
        response = requests.get(
            f"{BASE_URL}/relatorios/movimentacoes-por-tipo"
        )

        self.assertEqual(response.status_code, 200)

        dados = response.json()

        self.assertIsInstance(
            dados,
            list
        )

        print("[OK] Relatório de movimentações")

    # TESTES DE ERRO

    def test_20_produto_inexistente(self):
        response = requests.get(
            f"{BASE_URL}/produtos/999999999"
        )

        self.assertEqual(
            response.status_code,
            404
        )

        dados = response.json()

        self.assertIn(
            "erro",
            dados
        )

        print("[OK] Produto inexistente → 404")

    def test_21_eletronico_inexistente(self):
        response = requests.get(
            f"{BASE_URL}/eletronicos/999999999"
        )

        self.assertEqual(
            response.status_code,
            404
        )

        print("[OK] Eletrônico inexistente → 404")

    def test_22_venda_inexistente(self):
        response = requests.get(
            f"{BASE_URL}/vendas/999999999"
        )

        self.assertEqual(
            response.status_code,
            404
        )

        print("[OK] Venda inexistente → 404")

    def test_23_produto_sem_dados(self):
        response = requests.post(
            f"{BASE_URL}/produtos",
            json={}
        )

        self.assertEqual(
            response.status_code,
            400
        )

        print("[OK] Produto sem dados → 400")

    def test_24_venda_quantidade_zero(self):
        dados = {
            "id_produto": TestAPI.produto_id,
            "quantidade": 0,
            "preco_unitario": 100
        }

        response = requests.post(
            f"{BASE_URL}/vendas",
            json=dados
        )

        self.assertEqual(
            response.status_code,
            400
        )

        print("[OK] Venda com quantidade zero → 400")

    def test_25_venda_preco_zero(self):
        dados = {
            "id_produto": TestAPI.produto_id,
            "quantidade": 1,
            "preco_unitario": 0
        }

        response = requests.post(
            f"{BASE_URL}/vendas",
            json=dados
        )

        self.assertEqual(
            response.status_code,
            400
        )

        print("[OK] Venda com preço zero → 400")

    # LIMPEZA

    @classmethod
    def tearDownClass(cls):
        """
        Remove somente os dados criados pelos testes.
        """

        print("\nLimpando dados criados pelos testes.")

        # Primeiro remove a venda
        if cls.venda_id is not None:
            response = requests.delete(
                f"{BASE_URL}/vendas/{cls.venda_id}"
            )

            if response.status_code == 200:
                print("[OK] Venda de teste removida")

        # Depois remove o eletrônico
        if cls.eletronico_id is not None:
            response = requests.delete(
                f"{BASE_URL}/eletronicos/{cls.eletronico_id}"
            )

            if response.status_code == 200:
                print("[OK] Eletrônico de teste removido")

        # Por último remove o produto
        if cls.produto_id is not None:
            response = requests.delete(
                f"{BASE_URL}/produtos/{cls.produto_id}"
            )

            if response.status_code == 200:
                print("[OK] Produto de teste removido")

        print("TESTES FINALIZADOS")


if __name__ == "__main__":
    unittest.main(verbosity=0)



