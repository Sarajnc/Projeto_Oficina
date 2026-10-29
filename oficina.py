
from estruturas import ListaEncadeada, Fila, ArvoreComponente
from cadastro import ControleCadastro
from estoque import ControleEstoque
from pagamento import ControleFinanceiro
from atendimento import Atendimento

class OrdemServico:
    def __init__(self, atendimento, id_os):
        self.id_os = id_os
        self.atendimento = atendimento
        self.diagnostico = ListaEncadeada()
        self.servicos = ListaEncadeada()
        self.status = "Aberta"
        self.valor_total = 0.0
        self.remontagem_concluida = False

        self.arvore_componentes = ArvoreComponente()
        self.arvore_componentes.montar_arvore()

        self.pecas_utilizadas = ListaEncadeada()

class Servico:
    def __init__(self, descricao, valor):
        self.descricao = descricao
        self.valor = float(valor)

class ControleOficina(ControleEstoque, ControleCadastro, ControleFinanceiro):
    def __init__(self):
        ControleCadastro.__init__(self)
        ControleEstoque.__init__(self)
        ControleFinanceiro.__init__(self)

        self.total_elevadores = 2
        self.elevadores_ocupados = 0

        self.fila_normal = Fila()
        self.fila_guincho = Fila()

        self.atendimentos_em_andamento = ListaEncadeada()
        self.ordens_servico = ListaEncadeada()

        self.proximo_id_os = 1

    def buscar_atendimento(self, placa):
        atual = self.atendimentos_em_andamento.inicio

        while atual is not None:
            if atual.dado.placa.upper() == placa.upper():
                return atual.dado
            atual = atual.proximo

        return None

    def buscar_os(self, id_os):
        atual = self.ordens_servico.inicio

        while atual is not None:
            if atual.dado.id_os == int(id_os):
                return atual.dado
            atual = atual.proximo

        return None

    def registrar_chegada(self, placa, tipo_chegada, queixa):
        veiculo = self.buscar_veiculo(placa)

        if veiculo is None:
            print("Veículo não encontrado!")
            return False

        if self.buscar_atendimento(placa) is not None:
            print("Este veículo já está em atendimento!")
            return False

        tipo_chegada = tipo_chegada.strip().lower()

        if tipo_chegada not in ("guincho", "normal"):
            print("Tipo de chegada inválido!")
            return False

        cliente = self.clientes.inicio

        while cliente is not None:
            if cliente.dado.idcliente == veiculo.idcliente:
                break
            cliente = cliente.proximo

        if cliente is None:
            print("Cliente associado ao veículo não encontrado!")
            return False

        atendimento = Atendimento(
            veiculo.placa,
            cliente.dado.nome,
            queixa
        )

        if tipo_chegada == "guincho":
            self.fila_guincho.enfileirar(atendimento)
        else:
            self.fila_normal.enfileirar(atendimento)

        print("Chegada registrada com sucesso!")
        return True

    def chamar_proximo(self):
        if self.elevadores_ocupados >= self.total_elevadores:
            print("Todos os elevadores estão ocupados!")
            return None

        if not self.fila_guincho.esta_vazia():
            atendimento = self.fila_guincho.desenfileirar()
        elif not self.fila_normal.esta_vazia():
            atendimento = self.fila_normal.desenfileirar()
        else:
            print("Não há veículos na fila!")
            return None

        self.atendimentos_em_andamento.adicionar(atendimento)
        self.elevadores_ocupados += 1

        print("Veículo chamado:", atendimento.placa)
        print("Cliente:", atendimento.nome_cliente)
        print("Queixa:", atendimento.queixa)

        return atendimento

    def liberar_elevador(self, placa):
        atendimento = self.buscar_atendimento(placa)

        if atendimento is None:
            print("Não existe atendimento em andamento para essa placa!")
            return False

        # Não libera o elevador se ainda houver uma OS aberta.
        atual = self.ordens_servico.inicio

        while atual is not None:
            ordem = atual.dado

            if (ordem.atendimento.placa.upper() == placa.upper()
                    and ordem.status == "Aberta"):
                print("Não é possível liberar: existe uma OS aberta!")
                return False

            atual = atual.proximo

        self.atendimentos_em_andamento.remover(atendimento)
        self.elevadores_ocupados -= 1

        print("Atendimento finalizado para o veículo:", placa)
        print("Elevador disponível!")
        return True

    def abrir_ordem_servico(self, placa):
        atendimento = self.buscar_atendimento(placa)

        if atendimento is None:
            print("Veículo não possui atendimento em andamento!")
            return None

        # Evita duas ordens abertas para o mesmo veículo.
        atual = self.ordens_servico.inicio

        while atual is not None:
            ordem_existente = atual.dado

            if (ordem_existente.atendimento.placa.upper() == placa.upper()
                    and ordem_existente.status == "Aberta"):
                print("Este veículo já possui uma OS aberta!")
                return None

            atual = atual.proximo

        ordem = OrdemServico(atendimento, self.proximo_id_os)
        self.ordens_servico.adicionar(ordem)
        self.proximo_id_os += 1

        print("Ordem de serviço criada!")
        print("Número da OS:", ordem.id_os)

        return ordem

    def registrar_diagnostico(self, id_os, nome_componente):
        ordem = self.buscar_os(id_os)

        if ordem is None:
            print("Ordem de serviço não encontrada!")
            return False

        if ordem.status != "Aberta":
            print("A ordem de serviço não está aberta!")
            return False

        componente = ordem.arvore_componentes.buscar_componente(
            ordem.arvore_componentes.raiz,
            nome_componente
        )

        if componente is None:
            print("Componente não encontrado!")
            return False

        componente.estado = "Com defeito"

        if not ordem.diagnostico.contem(nome_componente):
            ordem.diagnostico.adicionar(nome_componente)

        print("Diagnóstico registrado!")
        return True

    def mostrar_arvore_componentes(self, id_os):
        ordem = self.buscar_os(id_os)

        if ordem is None:
            print("Ordem de serviço não encontrada!")
            return

        ordem.arvore_componentes.mostrar_arvore()

    def adicionar_servico(self, id_os, descricao, valor):
        ordem = self.buscar_os(id_os)

        if ordem is None:
            print("Ordem de serviço não encontrada!")
            return False

        if ordem.status != "Aberta":
            print("A ordem de serviço não está aberta!")
            return False

        if float(valor) < 0:
            print("O valor não pode ser negativo!")
            return False

        servico = Servico(descricao, valor)
        ordem.servicos.adicionar(servico)
        ordem.valor_total += servico.valor

        print("Serviço adicionado com sucesso!")
        print("Valor total da OS: R$", round(ordem.valor_total, 2))
        return True

    def adicionar_peca_ordem_servico(self, id_os, codigo, quantidade):
        ordem = self.buscar_os(id_os)

        if ordem is None:
            print("Ordem de serviço não encontrada!")
            return False

        if ordem.status != "Aberta":
            print("A ordem de serviço não está aberta!")
            return False

        try:
            quantidade = int(quantidade)
        except (ValueError, TypeError):
            print("A quantidade deve ser um número inteiro!")
            return False

        if quantidade <= 0:
            print("A quantidade deve ser positiva!")
            return False

        peca = self.buscar_peca(codigo)

        if peca is None:
            print("Peça não encontrada!")
            return False

        disponivel = self._quantidade_total(peca)

        if disponivel < quantidade:
            print("Estoque insuficiente!")
            return False

        # Calcula o preço usando os lotes mais antigos primeiro.
        restante = quantidade
        valor_total_pecas = 0.0
        lote_atual = peca.lotes.inicio

        while lote_atual is not None and restante > 0:
            lote = lote_atual.dado
            usar = min(restante, lote.quantidade)

            valor_total_pecas += usar * lote.preco_venda
            restante -= usar
            lote_atual = lote_atual.proximo

        if restante > 0:
            print("Não foi possível calcular o valor da peça!")
            return False

        sucesso = self.retirar_estoque(codigo, quantidade)

        if sucesso is False:
            return False

        valor_unitario = valor_total_pecas / quantidade

        item = {
            "codigo": peca.codigo,
            "descricao": peca.descricao,
            "quantidade": quantidade,
            "valor_unitario": valor_unitario,
            "subtotal": valor_total_pecas
        }

        ordem.pecas_utilizadas.adicionar(item)
        ordem.valor_total += valor_total_pecas

        print("Peça adicionada à ordem de serviço!")
        print("Peça:", peca.descricao)
        print("Quantidade:", quantidade)
        print("Valor das peças: R$", round(valor_total_pecas, 2))
        print("Total da OS: R$", round(ordem.valor_total, 2))

        return True

    def registrar_remontagem(self, id_os):
        ordem = self.buscar_os(id_os)

        if ordem is None:
            print("Ordem de serviço não encontrada!")
            return False

        if ordem.status != "Aberta":
            print("A ordem de serviço não está aberta!")
            return False

        ordem.remontagem_concluida = True
        print("Remontagem registrada com sucesso!")
        return True

    def fechar_ordem_servico(self, id_os, forma_pagamento=None):
        ordem = self.buscar_os(id_os)

        if ordem is None:
            print("Ordem de serviço não encontrada!")
            return False

        if ordem.status != "Aberta":
            print("A ordem de serviço já foi encerrada!")
            return False

        if not ordem.remontagem_concluida:
            print("Registre a remontagem antes de fechar a OS!")
            return False

        if ordem.servicos.esta_vazia() and ordem.pecas_utilizadas.esta_vazia():
            print("Adicione pelo menos um serviço ou uma peça antes de fechar a OS!")
            return False

        if self.buscar_atendimento(ordem.atendimento.placa) is None:
            print("Veículo não está em atendimento!")
            return False

        if forma_pagamento is None:
            forma_pagamento = input(
                "Forma de pagamento (PIX, Cartão ou Dinheiro): "
            )

        resultado = self.registrar_pagamento(
            ordem.id_os,
            ordem.valor_total,
            forma_pagamento
        )

        if resultado is False:
            return False

        ordem.status = "Concluída"

        print("Ordem de serviço concluída!")
        print("Número da OS:", ordem.id_os)
        print("Valor final: R$", round(ordem.valor_total, 2))

        self.liberar_elevador(ordem.atendimento.placa)

        return True

    def mostrar_ordens_servico(self):
        atual = self.ordens_servico.inicio

        if atual is None:
            print("Nenhuma ordem de serviço cadastrada.")
            return

        while atual is not None:
            ordem = atual.dado

            print(
                f"OS: {ordem.id_os} | "
                f"Placa: {ordem.atendimento.placa} | "
                f"Cliente: {ordem.atendimento.nome_cliente} | "
                f"Status: {ordem.status} | "
                f"Total: R$ {ordem.valor_total:.2f}"
            )

            atual = atual.proximo
