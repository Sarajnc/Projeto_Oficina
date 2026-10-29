
from estruturas import ListaEncadeada, Fila
from datetime import datetime

class LoteEstoque:
    def __init__(
        self,
        quantidade,
        fornecedor,
        preco_compra,
        data_entrada,
        data_validade=None
    ):
        self.quantidade = quantidade
        self.fornecedor = fornecedor
        self.preco_compra = preco_compra
        self.data_entrada = data_entrada
        self.data_validade = data_validade

class Peca:
    def __init__(
        self,
        codigo,
        descricao,
        preco_venda=0.0,
        estoque_minimo=0
    ):
        self.codigo = codigo
        self.descricao = descricao
        self.preco_venda = preco_venda
        self.estoque_minimo = estoque_minimo
        self.lotes = Fila()

class RegistroPerda:
    def __init__(
        self,
        codigo,
        descricao,
        quantidade,
        fornecedor,
        data_validade,
        preco_compra,
        motivo
    ):
        self.codigo = codigo
        self.descricao = descricao
        self.quantidade = quantidade
        self.fornecedor = fornecedor
        self.data_validade = data_validade
        self.preco_compra = preco_compra
        self.valor_perda = quantidade * preco_compra
        self.motivo = motivo
        self.data_registro = datetime.now()

class ControleEstoque:
    def __init__(self):
        self.estoque = ListaEncadeada()
        self.perdas = ListaEncadeada()

    def buscar_peca(self, codigo):
        atual = self.estoque.inicio

        while atual is not None:
            if atual.dado.codigo == codigo:
                return atual.dado
            atual = atual.proximo

        return None

    def cadastrar_peca(
        self, codigo, descricao, preco_venda=0.0, estoque_minimo=0
    ):
        if self.buscar_peca(codigo) is not None:
            print("Código de peça já cadastrado!")
            return False

        if preco_venda < 0 or estoque_minimo < 0:
            print("Os valores não podem ser negativos!")
            return False

        peca = Peca(codigo, descricao, preco_venda, estoque_minimo)
        self.estoque.adicionar(peca)

        print("Peça cadastrada com sucesso!")
        return True

    def registrar_entrada_estoque(
        self,
        codigo,
        quantidade,
        fornecedor,
        preco_compra,
        data_validade=None
    ):
        peca = self.buscar_peca(codigo)

        if peca is None:
            print("Peça não encontrada!")
            return False

        if not isinstance(quantidade, int) or isinstance(quantidade, bool) or quantidade <= 0:
            print("A quantidade deve ser um número inteiro positivo!")
            return False

        try:
            preco_compra = float(preco_compra)
        except (ValueError, TypeError):
            print("Preço de compra inválido!")
            return False

        if preco_compra < 0:
            print("O preço de compra não pode ser negativo!")
            return False

        if not isinstance(fornecedor, str) or not fornecedor.strip():
            print("Informe o fornecedor!")
            return False

        if data_validade:
            if isinstance(data_validade, str):
                try:
                    data_validade = datetime.strptime(
                        data_validade, "%d/%m/%Y"
                    )
                except ValueError:
                    print("Data inválida! Use DD/MM/AAAA.")
                    return False
            elif not isinstance(data_validade, datetime):
                print("A validade deve ser uma data no formato DD/MM/AAAA.")
                return False

        lote = LoteEstoque(
            quantidade,
            fornecedor.strip(),
            preco_compra,
            datetime.now(),
            data_validade
        )

        peca.lotes.enfileirar(lote)

        print("Entrada registrada com sucesso!")
        print("Peça:", peca.descricao)
        print("Quantidade recebida:", quantidade)

        self.verificar_estoque_minimo(codigo)
        return True

    def _quantidade_total(self, peca):
        total = 0
        atual = peca.lotes.inicio

        while atual is not None:
            total += atual.dado.quantidade
            atual = atual.proximo

        return total

    def _baixar_quantidade(self, peca, quantidade):
        if quantidade < 0 or self._quantidade_total(peca) < quantidade:
            return False

        restante = quantidade

        while restante > 0:
            if peca.lotes.inicio is None:
                return False

            lote = peca.lotes.inicio.dado

            if lote.quantidade <= restante:
                restante -= lote.quantidade
                peca.lotes.desenfileirar()
            else:
                lote.quantidade -= restante
                restante = 0

        return True

    def consultar_estoque(self, codigo):
        self.descartar_lotes_vencidos()

        peca = self.buscar_peca(codigo)

        if peca is None:
            print("Peça não encontrada!")
            return None

        quantidade = self._quantidade_total(peca)

        print("Peça:", peca.descricao)
        print("Quantidade disponível:", quantidade)

        self.verificar_estoque_minimo(codigo)
        return quantidade

    def retirar_estoque(self, codigo, quantidade):
        if (
            not isinstance(quantidade, int)
            or isinstance(quantidade, bool)
            or quantidade <= 0
        ):
            print("A quantidade deve ser um número inteiro positivo!")
            return False

        self.descartar_lotes_vencidos()

        peca = self.buscar_peca(codigo)

        if peca is None:
            print("Peça não encontrada!")
            return False

        disponivel = self._quantidade_total(peca)

        if disponivel < quantidade:
            print("Estoque insuficiente!")
            return False

        if not self._baixar_quantidade(peca, quantidade):
            print("Não foi possível retirar as peças!")
            return False

        print("Retirada registrada com sucesso!")
        print("Peça:", peca.descricao)
        print("Quantidade retirada:", quantidade)

        self.verificar_estoque_minimo(codigo)
        return True

    def descartar_lotes_vencidos(self):
        hoje = datetime.now().date()
        atual_peca = self.estoque.inicio
        total_descartado = 0

        while atual_peca is not None:
            peca = atual_peca.dado
            fila_nova = Fila()

            while not peca.lotes.esta_vazia():
                lote = peca.lotes.desenfileirar()
                validade = lote.data_validade

                if isinstance(validade, datetime):
                    validade = validade.date()

                if validade is not None and validade < hoje:
                    perda = RegistroPerda(
                        peca.codigo,
                        peca.descricao,
                        lote.quantidade,
                        lote.fornecedor,
                        lote.data_validade,
                        lote.preco_compra,
                        "Lote vencido"
                    )

                    self.perdas.adicionar(perda)
                    total_descartado += 1

                    print(
                        "Lote vencido descartado:",
                        peca.descricao,
                        "| Quantidade:",
                        lote.quantidade
                    )
                else:
                    fila_nova.enfileirar(lote)

            peca.lotes = fila_nova
            atual_peca = atual_peca.proximo

        if total_descartado == 0:
            print("Nenhum lote vencido encontrado.")
        else:
            print("Lotes descartados:", total_descartado)

        return total_descartado

    def ajustar_estoque(self, codigo, nova_quantidade):
        if (
            not isinstance(nova_quantidade, int)
            or isinstance(nova_quantidade, bool)
            or nova_quantidade < 0
        ):
            print("Informe uma quantidade inteira igual ou maior que zero!")
            return False

        self.descartar_lotes_vencidos()

        peca = self.buscar_peca(codigo)

        if peca is None:
            print("Peça não encontrada!")
            return False

        quantidade_atual = self._quantidade_total(peca)

        if nova_quantidade == quantidade_atual:
            print("O estoque já possui essa quantidade.")
            return True

        if nova_quantidade > quantidade_atual:
            diferenca = nova_quantidade - quantidade_atual

            lote_ajuste = LoteEstoque(
                diferenca,
                "Ajuste de inventário",
                0.0,
                datetime.now(),
                None
            )

            peca.lotes.enfileirar(lote_ajuste)
        else:
            diferenca = quantidade_atual - nova_quantidade

            if not self._baixar_quantidade(peca, diferenca):
                print("Não foi possível ajustar o estoque!")
                return False

        print("Inventário ajustado com sucesso!")
        print("Quantidade anterior:", quantidade_atual)
        print("Quantidade atual:", nova_quantidade)

        self.verificar_estoque_minimo(codigo)
        return True

    def verificar_estoque_minimo(self, codigo=None):
        if codigo is not None:
            peca = self.buscar_peca(codigo)

            if peca is None:
                print("Peça não encontrada!")
                return None

            quantidade = self._quantidade_total(peca)

            if quantidade < peca.estoque_minimo:
                print(
                    "ALERTA: estoque abaixo do mínimo para",
                    peca.descricao,
                    "| Disponível:", quantidade,
                    "| Mínimo:", peca.estoque_minimo
                )

            return quantidade

        atual = self.estoque.inicio

        while atual is not None:
            peca = atual.dado
            quantidade = self._quantidade_total(peca)

            if quantidade < peca.estoque_minimo:
                print(
                    "ALERTA: estoque abaixo do mínimo para",
                    peca.descricao,
                    "| Disponível:", quantidade,
                    "| Mínimo:", peca.estoque_minimo
                )

            atual = atual.proximo

    def mostrar_perdas(self):
        atual = self.perdas.inicio

        if atual is None:
            print("Nenhuma perda registrada.")
            return

        print("=== REGISTRO DE PERDAS ===")

        while atual is not None:
            perda = atual.dado

            print("Peça:", perda.descricao)
            print("Código:", perda.codigo)
            print("Quantidade descartada:", perda.quantidade)
            print("Fornecedor:", perda.fornecedor)
            print("Motivo:", perda.motivo)
            print("Valor estimado da perda: R$", perda.valor_perda)
            print(
                "Data do registro:",
                perda.data_registro.strftime("%d/%m/%Y %H:%M")
            )
            print("---------------------------")

            atual = atual.proximo