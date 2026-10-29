
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

class ControleCadastro:
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
        if not nome.strip() or not cpf.strip() or not telefone.strip():
            print("Preencha todos os campos do cliente!")
            return False

        if self.buscar_cliente(cpf) is not None:
            print("O CPF informado já está cadastrado!")
            return False

        novo_cliente = Cliente(
            nome.strip(),
            cpf.strip(),
            telefone.strip(),
            self.proximo_id
        )

        self.clientes.adicionar(novo_cliente)
        self.proximo_id += 1

        print("Cliente cadastrado com sucesso!")
        return True

    def buscar_veiculo(self, placa):
        atual = self.veiculos.inicio

        while atual is not None:
            if atual.dado.placa.upper() == placa.upper():
                return atual.dado

            atual = atual.proximo

        return None

    def remover_veiculo(self, placa):
        veiculo = self.buscar_veiculo(placa)

        if veiculo is None:
            print("Veículo não encontrado!")
            return False

        self.veiculos.remover(veiculo)

        atual = self.clientes.inicio

        while atual is not None:
            cliente = atual.dado

            if cliente.idcliente == veiculo.idcliente:
                cliente.veiculos.remover(veiculo)
                break

            atual = atual.proximo

        print("Veículo removido com sucesso!")
        return True

    def cadastrar_veiculo(self, cpf, placa, modelo, marca, ano):
        if not all(
            isinstance(campo, str) and campo.strip()
            for campo in (cpf, placa, modelo, marca)
        ):
            print("Preencha todos os campos do veículo!")
            return False

        placa = placa.strip().upper()
        cliente = self.buscar_cliente(cpf.strip())

        if cliente is None:
            print("Cliente não encontrado!")
            return False

        if self.buscar_veiculo(placa) is not None:
            print("A placa informada já está cadastrada!")
            return False

        try:
            ano = int(ano)
        except (ValueError, TypeError):
            print("O ano deve ser um número inteiro!")
            return False

        if ano <= 0:
            print("Informe um ano válido!")
            return False

        novo_veiculo = Veiculo(
            placa,
            modelo.strip(),
            marca.strip(),
            ano,
            cliente.idcliente
        )

        self.veiculos.adicionar(novo_veiculo)
        cliente.veiculos.adicionar(novo_veiculo)

        print("Veículo cadastrado com sucesso!")
        return True