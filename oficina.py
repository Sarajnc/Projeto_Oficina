from estruturas import ListaEncadeada

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
        self.veiculos = ListaEncadeada()

class ControleOficina:
    def __init__(self):
    
        self.clientes = ListaEncadeada()
        self.veiculos = ListaEncadeada()

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
            return

        novo_cliente = Cliente(nome, cpf, telefone, self.proximo_id)
        self.clientes.adicionar(novo_cliente)
        self.proximo_id += 1

    def cadastrar_veiculo(self, cpf, placa, modelo, marca, ano):
        cliente = self.buscar_cliente(cpf)

        if cliente is None:
            print("Cliente não encontrado")
            return

        novo_veiculo = Veiculo(placa, modelo, marca, ano, cliente.idcliente)
        self.veiculos.adicionar(novo_veiculo)
