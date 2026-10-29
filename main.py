
from oficina import ControleOficina

def main():
    oficina = ControleOficina()

    while True:
        print("\n===== SISTEMA DE OFICINA MECÂNICA =====")
        print("1 - Cadastrar cliente")
        print("2 - Cadastrar veículo")
        print("3 - Registrar chegada")
        print("4 - Chamar próximo veículo")
        print("5 - Abrir ordem de serviço")
        print("6 - Registrar diagnóstico")
        print("7 - Mostrar árvore de componentes")
        print("8 - Adicionar serviço")
        print("9 - Cadastrar peça")
        print("10 - Registrar entrada de estoque")
        print("11 - Adicionar peça à OS")
        print("12 - Registrar remontagem")
        print("13 - Fechar ordem de serviço")
        print("14 - Consultar estoque")
        print("15 - Mostrar ordens de serviço")
        print("16 - Mostrar perdas de estoque")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome do cliente: ")
            cpf = input("CPF: ")
            telefone = input("Telefone: ")
            oficina.cadastrar_cliente(nome, cpf, telefone)

        elif opcao == "2":
            cpf = input("CPF do proprietário: ")
            placa = input("Placa: ")
            modelo = input("Modelo: ")
            marca = input("Marca: ")
            ano = input("Ano: ")
            oficina.cadastrar_veiculo(cpf, placa, modelo, marca, ano)

        elif opcao == "3":
            placa = input("Placa do veículo: ")
            tipo = input("Tipo de chegada (normal/guincho): ")
            queixa = input("Problema relatado: ")
            oficina.registrar_chegada(placa, tipo, queixa)

        elif opcao == "4":
            oficina.chamar_proximo()

        elif opcao == "5":
            placa = input("Placa do veículo: ")
            oficina.abrir_ordem_servico(placa)

        elif opcao == "6":
            id_os = input("Número da OS: ")
            componente = input("Nome do componente: ")
            oficina.registrar_diagnostico(id_os, componente)

        elif opcao == "7":
            id_os = input("Número da OS: ")
            oficina.mostrar_arvore_componentes(id_os)

        elif opcao == "8":
            id_os = input("Número da OS: ")
            descricao = input("Descrição do serviço: ")

            try:
                valor = float(input("Valor do serviço: R$ "))
                oficina.adicionar_servico(id_os, descricao, valor)
            except ValueError:
                print("Informe um valor numérico válido!")

        elif opcao == "9":
            codigo = input("Código da peça: ")
            descricao = input("Descrição da peça: ")

            try:
                preco = float(input("Preço de venda: R$ "))
                minimo = int(input("Estoque mínimo: "))
                oficina.cadastrar_peca(
                    codigo, descricao, preco, minimo
                )
            except ValueError:
                print("Preço ou estoque mínimo inválido!")

        elif opcao == "10":
            codigo = input("Código da peça: ")

            try:
                quantidade = int(input("Quantidade recebida: "))
                preco = float(input("Preço de compra por unidade: R$ "))
            except ValueError:
                print("Quantidade ou preço inválido!")
                continue

            fornecedor = input("Fornecedor: ")
            validade = input(
                "Validade (DD/MM/AAAA) ou Enter se não houver: "
            ).strip()

            oficina.registrar_entrada_estoque(
                codigo,
                quantidade,
                fornecedor,
                preco,
                validade if validade else None
            )

        elif opcao == "11":
            id_os = input("Número da OS: ")
            codigo = input("Código da peça: ")

            try:
                quantidade = int(input("Quantidade: "))
                oficina.adicionar_peca_ordem_servico(
                    id_os, codigo, quantidade
                )
            except ValueError:
                print("Quantidade inválida!")

        elif opcao == "12":
            id_os = input("Número da OS: ")
            oficina.registrar_remontagem(id_os)

        elif opcao == "13":
            id_os = input("Número da OS: ")
            forma = input(
                "Forma de pagamento (PIX, Cartão ou Dinheiro): "
            )
            oficina.fechar_ordem_servico(id_os, forma)

        elif opcao == "14":
            codigo = input("Código da peça: ")
            oficina.consultar_estoque(codigo)

        elif opcao == "15":
            oficina.mostrar_ordens_servico()

        elif opcao == "16":
            oficina.descartar_lotes_vencidos()
            oficina.mostrar_perdas()

        elif opcao == "0":
            print("Sistema encerrado.")
            break

        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
