
from estruturas import ListaEncadeada

class Pagamento:
    def __init__(self, id_os, valor, forma_pagamento):
        self.id_os = id_os
        self.valor = float(valor)
        self.forma_pagamento = forma_pagamento
        self.status = "Pendente"

class ControleFinanceiro:
    def __init__(self):
        self.pagamentos = ListaEncadeada()

    def registrar_pagamento(self, id_os, valor, forma_pagamento):
        try:
            valor = float(valor)
        except (ValueError, TypeError):
            print("Valor de pagamento inválido!")
            return False

        if valor <= 0:
            print("O valor deve ser maior que zero!")
            return False

        formas_validas = ("pix", "cartão", "cartao", "dinheiro")
        forma = forma_pagamento.strip().lower()

        if forma not in formas_validas:
            print("Forma inválida! Use PIX, Cartão ou Dinheiro.")
            return False

        if forma == "cartao":
            forma_pagamento = "Cartão"
        elif forma == "pix":
            forma_pagamento = "PIX"
        else:
            forma_pagamento = "Dinheiro"

        pagamento = Pagamento(id_os, valor, forma_pagamento)
        pagamento.status = "Pago"

        self.pagamentos.adicionar(pagamento)

        print("Pagamento registrado com sucesso!")
        print("OS:", id_os)
        print(f"Valor: R$ {valor:.2f}")
        print("Forma de pagamento:", forma_pagamento)

        return True

    def mostrar_pagamentos(self):
        if self.pagamentos.esta_vazia():
            print("Nenhum pagamento registrado.")
            return

        atual = self.pagamentos.inicio

        while atual is not None:
            pagamento = atual.dado

            print(
                f"OS: {pagamento.id_os} | "
                f"Valor: R$ {pagamento.valor:.2f} | "
                f"Forma: {pagamento.forma_pagamento} | "
                f"Status: {pagamento.status}"
            )

            atual = atual.proximo
