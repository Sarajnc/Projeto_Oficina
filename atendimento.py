from datetime import datetime

class Atendimento:
    def __init__(self, placa, nome_cliente, queixa):
        self.placa = placa
        self.nome_cliente = nome_cliente
        self.queixa = queixa
        self.data_hora = datetime.now()
