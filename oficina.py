from estruturas import ListaEncadeada, Fila
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

class ControleOficina:
    def __init__(self):
    
        self.clientes = ListaEncadeada()
        self.veiculos = ListaEncadeada()

        self.total_elevadores = 2
        self.elevadores_ocupados = 0
        
        self.fila_normal = Fila()
        self.fila_guincho = Fila()

        self.proximo_id = 1 

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
        else: 
            cliente = self.buscar_cliente(cpf)

        if cliente is None:
            print("Cliente não encontrado")
        else:
            novo_veiculo = Veiculo(placa, modelo, marca, ano, cliente.idcliente)
            self.veiculos.adicionar(novo_veiculo)        

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

        print("Veículo chamado:", atendimento.placa)
        print("Cliente:", atendimento.nome_cliente)
        print("Queixa:", atendimento.queixa)

    def liberar_elevador(self):
        if self.elevadores_ocupados > 0:
            self.elevadores_ocupados -= 1
            print("Elevador disponível!")
        else:
            print("Os elevadores estõa livres")