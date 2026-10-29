class No:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None

class Fila:
    def __init__(self):
        self.inicio = None
        self.fim = None

    def enfileirar(self, dado):
        novo_no = No(dado)

        if self.fim is None:
            self.inicio = novo_no
            self.fim = novo_no
        else:
            self.fim.proximo = novo_no
            self.fim = novo_no

    def desenfileirar(self):
        if self.inicio is None:
            return None
        else:
            dado = self.inicio.dado
            self.inicio = self.inicio.proximo

            if self.inicio is None:
                self.fim = None

            return dado

    def esta_vazia(self):
        return self.inicio is None

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

class NoArvore:
    def __init__(self, componente, codigo_peca = None, estado = "OK"):
        self.componente = componente
        self.codigo_peca = codigo_peca
        self.estado = estado
        self.filhos = ListaEncadeada()

    def adicionar_filho(self,filho):
        self.filhos.adicionar(filho)

class ArvoreComponente:
    def __init__(self):
        self.raiz = NoArvore("Veiculo")

    def montar_arvore(self):
        motor = NoArvore("Motor")
        freios = NoArvore("Freios")
        suspensao = NoArvore("Suspensão")

        self.raiz.adicionar_filho(motor)
        self.raiz.adicionar_filho(freios)
        self.raiz.adicionar_filho(suspensao)

        # Motor
        ignicao = NoArvore("Sistema de ignição")
        correia = NoArvore("Correia dentada")

        motor.adicionar_filho(ignicao)
        motor.adicionar_filho(correia)

        # Sistema de ignição
        vela = NoArvore("Vela")
        bobina = NoArvore("Bobina")

        ignicao.adicionar_filho(vela)
        ignicao.adicionar_filho(bobina)

        # Freios
        pastilha = NoArvore("Pastilha dianteira")
        disco = NoArvore("Disco dianteiro")

        freios.adicionar_filho(pastilha)
        freios.adicionar_filho(disco)

        # Suspensão
        amortecedor = NoArvore("Amortecedor")
        bandeja = NoArvore("Bandeja")

        suspensao.adicionar_filho(amortecedor)
        suspensao.adicionar_filho(bandeja)

    def mostrar_arvore(self):
        self._mostrar_no(self.raiz, 0)

    def _mostrar_no(self, no, nivel):
        texto = " " * (nivel * 4) + no.componente
        texto += " | Estado: " + no.estado

        if no.codigo_peca is not None:
            texto += " | Código: " + no.codigo_peca

        print(texto)

        atual = no.filhos.inicio

        while atual is not None:
            self._mostrar_no(atual.dado, nivel + 1)
            atual = atual.proximo

    def buscar_componente(self, no, nome):
        if no.componente.lower() == nome.lower():
            return no

        atual = no.filhos.inicio

        while atual is not None:
            encontrado = self.buscar_componente(atual.dado, nome)

            if encontrado is not None:
                return encontrado

            atual = atual.proximo

        return None

    def alterar_estado(self, nome, novo_estado):
        if novo_estado not in ("OK", "Com defeito"):
            print("Estado inválido!")
            return

        componente = self.buscar_componente(self.raiz, nome)

        if componente is None:
            print("Componente não encontrado!")
            return

        componente.estado = novo_estado
        print("Estado atualizado com sucesso!")