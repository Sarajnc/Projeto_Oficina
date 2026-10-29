from estruturas import ListaEncadeada, Fila, ArvoreComponente, Peca, LoteEstoque
from datetime import datetime

class Veiculo:
    def __init__(self, placa, modelo, marca, ano, idcliente):
        self.placa = placa
        self.modelo = modelo
        self.marca = marca
        self.ano = ano
        self.idcliente = idcliente

class Cliente:
    def __init__(self, nome, cpf, telefone, idcliente):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.idcliente = idcliente

class Atendimento:
    def __init__(self, placa, nome_cliente, queixa):
        self.placa = placa
        self.nome_cliente = nome_cliente
        self.queixa = queixa
        self.data_hora = datetime.now()

class OrdemServico:
    def __init__(self, atendimento, id_os):
        self.id_os = id_os
        self.atendimento = atendimento
        self.diagnostico = []
        self.servicos = []
        self.status = "Aberta"
        self.valor_total = 0.0

        self.arvore_componentes = ArvoreComponente()
        self.arvore_componentes.montar_arvore() 
        
        self.pecas_utilizadas = []

class Servico:
    def __init__(self, descricao, valor):
        self.descricao = descricao
        self.valor = valor

class RegistroPerda:
    def __init__(
        self, codigo, descricao, quantidade, fornecedor,
        data_validade, preco_compra, motivo
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

class ControleOficina:
    def __init__(self):
    
        self.clientes = ListaEncadeada()
        self.veiculos = ListaEncadeada()

        self.total_elevadores = 2
        self.elevadores_ocupados = 0
        
        self.fila_normal = Fila()
        self.fila_guincho = Fila()

        self.atendimentos_em_andamento = ListaEncadeada()

        self.ordens_servico = ListaEncadeada()

        self.estoque = ListaEncadeada()
        
        self.perdas = ListaEncadeada()

        self.proximo_id = 1 
        self.proximo_id_os = 1

    def buscar_cliente(self, cpf):
        atual = self.clientes.inicio

        while atual is not None:
            if atual.dado.cpf == cpf:
                return atual.dado

            atual = atual.proximo

        return None
    
    def cadastrar_cliente(self, nome, cpf, telefone):
        cliente = self.buscar_cliente(cpf)

        if cliente is not None:
            print("O CPF informado já está cadastrado!")
        else:
            novo_cliente = Cliente(nome, cpf, telefone, self.proximo_id)
            self.clientes.adicionar(novo_cliente)
            self.proximo_id += 1

    def buscar_veiculo(self, placa):
        atual = self.veiculos.inicio

        while atual is not None:
            if atual.dado.placa == placa:
                return atual.dado
            
            atual = atual.proximo

        return None

    def remover_veiculo(self,placa):
        veiculo = self.buscar_veiculo(placa)

        if veiculo is None:
            print("Veículo não encontrado!")
        else:
            self.veiculos.remover(veiculo)
            print("Veiculo removido com sucesso")


    def cadastrar_veiculo(self, cpf, placa, modelo, marca, ano):
        veiculo = self.buscar_veiculo(placa)

        if veiculo is not None:
            print("A placa informada já está cadastrada")
            return
        
        cliente = self.buscar_cliente(cpf)

        if cliente is None:
            print("Cliente não encontrado")
            return
        
        novo_veiculo = Veiculo(placa, modelo, marca, ano, cliente.idcliente)
        self.veiculos.adicionar(novo_veiculo)      
        print("Veículo cadastrado com sucesso!")  

    def registrar_chegada(self, placa, tipo_chegada, queixa):
        veiculo = self.buscar_veiculo(placa)

        if veiculo is None:
            print("Veículo não encontrado!")
            return
        
        tipo_chegada = tipo_chegada.lower()

        if tipo_chegada != "guincho" and tipo_chegada != "normal":
            print("Tipo de chegada inválida!")
            return

        cliente = self.clientes.inicio
        while cliente is not None:
            if cliente.dado.idcliente == veiculo.idcliente:
                break
            cliente = cliente.proximo

        atendimento = Atendimento(veiculo.placa, cliente.dado.nome, queixa)
        
        if tipo_chegada == "guincho":
            self.fila_guincho.enfileirar(atendimento)
        else:
            self.fila_normal.enfileirar(atendimento)

        print("Chegada registrada com sucesso!")        

    def chamar_proximo(self):
        if self.elevadores_ocupados >= self.total_elevadores:
            print("Todos os elevadores estão ocupados!")
            return

        if not self.fila_guincho.esta_vazia():
            atendimento = self.fila_guincho.desenfileirar()
        elif not self.fila_normal.esta_vazia():
            atendimento = self.fila_normal.desenfileirar()
        else:
            print("Não há veículos na fila")
            return
        
        self.elevadores_ocupados += 1 

        self.atendimentos_em_andamento.adicionar(atendimento)

        print("Veículo chamado:", atendimento.placa)
        print("Cliente:", atendimento.nome_cliente)
        print("Queixa:", atendimento.queixa)

    def liberar_elevador(self, placa):
        atual = self.atendimentos_em_andamento.inicio
        atendimento_encontrado = None

        while atual is not None:
            if atual.dado.placa == placa:
                atendimento_encontrado = atual.dado
                break

            atual = atual.proximo

        if atendimento_encontrado is None:
            print("Não existe atendimento em andamento para essa placa!")
            return

        self.atendimentos_em_andamento.remover(atendimento_encontrado)
        self.elevadores_ocupados -= 1

        print("Atendimento finalizado para o veículo:", placa)
        print("Elevador disponível!")

    
    def abrir_ordem_servico(self, placa):
        atual = self.atendimentos_em_andamento.inicio

        while atual is not None:
            atendimento = atual.dado

            if atendimento.placa == placa:
                ordem = OrdemServico(atendimento, self.proximo_id_os)
                self.ordens_servico.adicionar(ordem)
                self.proximo_id_os += 1

                print("Ordem de serviço criada!")
                print("Número da OS:", ordem.id_os)
                return ordem

            atual = atual.proximo

        print("Veículo não possui atendimento em andamento!")
        return None
    
    def registrar_diagnostico(self, id_os, nome_componente):
        atual = self.ordens_servico.inicio

        while atual is not None:
            ordem = atual.dado

            if ordem.id_os == id_os:
                componente = ordem.arvore_componentes.buscar_componente(ordem.arvore_componentes.raiz,nome_componente)

                if componente is None:
                    print("Componente não encontrado!")
                    return

                componente.estado = "Com defeito"

                if nome_componente not in ordem.diagnostico:
                    ordem.diagnostico.append(nome_componente)

                print("Diagnóstico registrado!")
                return

            atual = atual.proximo

        print("Ordem de serviço não encontrada!")

    def adicionar_servico(self, id_os, descricao, valor):
        atual = self.ordens_servico.inicio

        while atual is not None:
            ordem = atual.dado

            if ordem.id_os == id_os:
                if ordem.status != "Aberta":
                    print("A ordem de serviço não está aberta!")
                    return

                if valor < 0:
                    print("O valor não pode ser negativo!")
                    return

                servico = Servico(descricao, valor)
                ordem.servicos.append(servico)
                ordem.valor_total += valor

                print("Serviço adicionado com sucesso!")
                print("Valor total da OS: R$", ordem.valor_total)
                return

            atual = atual.proximo

        print("Ordem de serviço não encontrada!")

    def adicionar_peca_ordem_servico(self, id_os, codigo, quantidade):
        atual = self.ordens_servico.inicio

        while atual is not None:
            ordem = atual.dado

            if ordem.id_os == id_os:
                if ordem.status != "Aberta":
                    print("A ordem de serviço não está aberta!")
                    return

                peca = self.buscar_peca(codigo)

                if peca is None:
                    print("Peça não encontrada!")
                    return

                if not isinstance(quantidade, int) or quantidade <= 0:
                    print("A quantidade deve ser um inteiro positivo!")
                    return

                disponivel = self._quantidade_total(peca)

                if disponivel < quantidade:
                    print("Estoque insuficiente!")
                    return

                sucesso = self.retirar_estoque(codigo, quantidade)

                if not sucesso:
                    return

                ordem.pecas_utilizadas.append({
                    "codigo": peca.codigo,
                    "descricao": peca.descricao,
                    "quantidade": quantidade,
                    "valor_unitario": peca.preco_venda
                })

                valor_pecas = peca.preco_venda * quantidade
                ordem.valor_total += valor_pecas

                print("Peça adicionada à ordem de serviço!")
                print("Peça:", peca.descricao)
                print("Quantidade:", quantidade)
                print("Valor das peças: R$", valor_pecas)
                print("Total da OS: R$", ordem.valor_total)
                return

            atual = atual.proximo

    def fechar_ordem_servico(self, id_os):
        atual = self.ordens_servico.inicio

        while atual is not None:
            ordem = atual.dado

            if ordem.id_os == id_os:
                if ordem.status != "Aberta":
                    print("A ordem de serviço já foi encerrada!")
                    return

                if len(ordem.servicos) == 0:
                    print("Adicione pelo menos um serviço antes de fechar a OS!")
                    return

                placa = ordem.atendimento.placa
                atendimento = self.atendimentos_em_andamento.inicio

                while atendimento is not None:
                    if atendimento.dado.placa == placa:
                        break
                    atendimento = atendimento.proximo

                if atendimento is None:
                    print("Veículo não está em atendimento!")
                    return

                ordem.status = "Concluída"
                self.liberar_elevador(placa)

                print("Ordem de serviço concluída!")
                print("Número da OS:", ordem.id_os)
                print("Valor final: R$", ordem.valor_total)
                return

            atual = atual.proximo

        print("Ordem de serviço não encontrada!")

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
            return

        if preco_venda < 0 or estoque_minimo < 0:
            print("Os valores não podem ser negativos!")
            return

        peca = Peca(codigo, descricao, preco_venda, estoque_minimo)
        self.estoque.adicionar(peca)

        print("Peça cadastrada com sucesso!")

    def registrar_entrada_estoque(
        self, codigo, quantidade, fornecedor, preco_compra,
        data_validade=None
    ):
        peca = self.buscar_peca(codigo)

        if peca is None:
            print("Peça não encontrada!")
            return

        if not isinstance(quantidade, int) or quantidade <= 0:
            print("A quantidade deve ser um número inteiro positivo!")
            return

        if preco_compra < 0:
            print("O preço de compra não pode ser negativo!")
            return

        if not fornecedor.strip():
            print("Informe o fornecedor!")
            return

        if data_validade:
            try:
                data_validade = datetime.strptime(
                    data_validade, "%d/%m/%Y"
                )
            except ValueError:
                print("Data inválida! Use DD/MM/AAAA.")
                return

        lote = LoteEstoque(quantidade,fornecedor,preco_compra,datetime.now(),data_validade)

        peca.lotes.enfileirar(lote)

        print("Entrada registrada com sucesso!")
        print("Peça:", peca.descricao)
        print("Quantidade recebida:", quantidade)

        self.verificar_estoque_minimo(codigo)

    def _quantidade_total(self, peca):
        total = 0
        atual = peca.lotes.inicio

        while atual is not None:
            total += atual.dado.quantidade
            atual = atual.proximo

        return total

    def _baixar_quantidade(self, peca, quantidade):
        restante = quantidade

        while restante > 0:
            lote = peca.lotes.inicio.dado

            if lote.quantidade <= restante:
                restante -= lote.quantidade
                peca.lotes.desenfileirar()
            else:
                lote.quantidade -= restante
                restante = 0

    def consultar_estoque(self, codigo):
        self.descartar_lotes_vencidos()

        peca = self.buscar_peca(codigo)

        if peca is None:
            print("Peça não encontrada!")
            return

        quantidade = self._quantidade_total(peca)

        print("Peça:", peca.descricao)
        print("Quantidade disponível:", quantidade)

        self.verificar_estoque_minimo(codigo)

        return quantidade

    def retirar_estoque(self, codigo, quantidade):
        if not isinstance(quantidade, int) or quantidade <= 0:
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

        self._baixar_quantidade(peca, quantidade)

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

                if lote.data_validade is not None:
                    validade = lote.data_validade

                    if isinstance(validade, datetime):
                        validade = validade.date()

                    if validade < hoje:
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
                        continue

                fila_nova.enfileirar(lote)

            peca.lotes = fila_nova
            atual_peca = atual_peca.proximo

        if total_descartado == 0:
            print("Nenhum lote vencido encontrado.")
        else:
            print("Lotes descartados:", total_descartado)

        return total_descartado

    def ajustar_estoque(self, codigo, nova_quantidade):
        if (not isinstance(nova_quantidade, int)or nova_quantidade < 0):
            print("Informe uma quantidade inteira igual ou maior que zero!")
            return

        self.descartar_lotes_vencidos()

        peca = self.buscar_peca(codigo)

        if peca is None:
            print("Peça não encontrada!")
            return

        quantidade_atual = self._quantidade_total(peca)

        if nova_quantidade == quantidade_atual:
            print("O estoque já possui essa quantidade.")
            return

        if nova_quantidade > quantidade_atual:
            diferenca = nova_quantidade - quantidade_atual

            lote_ajuste = LoteEstoque(diferenca,"Ajuste de inventário",0.0,datetime.now(),None)

            peca.lotes.enfileirar(lote_ajuste)

        else:
            diferenca = quantidade_atual - nova_quantidade
            self._baixar_quantidade(peca, diferenca)

        print("Inventário ajustado com sucesso!")
        print("Quantidade anterior:", quantidade_atual)
        print("Quantidade atual:", nova_quantidade)

        self.verificar_estoque_minimo(codigo)

    def verificar_estoque_minimo(self, codigo=None):
        if codigo is not None:
            peca = self.buscar_peca(codigo)

            if peca is None:
                print("Peça não encontrada!")
                return

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