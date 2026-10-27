class No:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None

class ListaEncadeada:
    def __init__(self):
        self.inicio = None

    def adicionar(self, dado):
        novo_no = No(dado)

        if self.inicio is None:
            self.inicio = novo_no
        else:
            atual = self.inicio

            while atual.proximo is not None:
                atual = atual.proximo
            atual.proximo = novo_no

    def mostrar(self):
        atual = self.inicio

        while atual is not None:
            print(atual.dado)
            atual= atual.proximo

    def buscar(self, dado):
        atual = self.inicio

        while atual is not None:
            if atual.dado == dado:
                return atual
            atual = atual.proximo

        return None

    def remover(self, dado):
        atual = self.inicio
        anterior = None

        while atual is not None and atual.dado != dado:
            anterior = atual
            atual = atual.proximo

        if atual is None:
            return False
        if anterior is None:
            self.inicio = atual.proximo
        else:
            anterior.proximo = atual.proximo
            return True