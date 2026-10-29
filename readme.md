# Sistema de Oficina Mecânica

Projeto acadêmico desenvolvido em Python para a disciplina de Estrutura de Dados da FATEC Rio Claro.

O objetivo é simular o funcionamento de uma oficina mecânica, desde a chegada do veículo até o diagnóstico, a utilização de peças, o fechamento da ordem de serviço e o pagamento.

## Funcionalidades do sistema

- Cadastro, busca e remoção de clientes e veículos.
- Organização da fila de atendimento, com prioridade para veículos trazidos por guincho.
- Diagnóstico por meio de uma árvore de componentes.
- Abertura e acompanhamento de ordens de serviço.
- Registro de peças utilizadas e serviços de mão de obra.
- Controle de entrada, retirada e ajuste de estoque.
- Gerenciamento de lotes, validade das peças e registro de perdas.
- Controle de estoque mínimo.
- Registro de pagamentos relacionados às ordens de serviço.

## Organização dos arquivos

- `main.py`: inicialização do sistema.
- `estruturas.py`: implementação das estruturas de dados.
- `cadastro.py`: classes e operações relacionadas a clientes e veículos.
- `oficina.py`: atendimento, elevadores, diagnóstico e ordens de serviço.
- `estoque.py`: peças, lotes, movimentações e perdas.
- `pagamento.py`: registro e controle de pagamentos.

## Combinações de estruturas de dados

### 1. Filas de atendimento prioritário

**Estruturas envolvidas:** `Fila`.

**Classes e métodos:** `ControleOficina`, `Fila`, `registrar_chegada()` e `chamar_proximo()`.

O sistema utiliza duas filas: uma para veículos comuns e outra para veículos trazidos por guincho. A fila de guincho é consultada primeiro; quando está vazia, o próximo veículo é retirado da fila normal.

Essa combinação permite priorizar os atendimentos de guincho sem perder a ordem de chegada entre veículos da mesma fila. Usar uma única fila exigiria mecanismos adicionais para localizar e priorizar os veículos de guincho.

### 2. Produtos e lotes de estoque

**Estruturas envolvidas:** `ListaEncadeada` e `Fila`.

**Classes e métodos:** `ControleEstoque`, `Peca`, `LoteEstoque`, `buscar_peca()`, `registrar_entrada_estoque()`, `retirar_estoque()` e `_baixar_quantidade()`.

O estoque mantém os produtos em uma lista encadeada, e cada produto possui uma fila de lotes. Quando ocorre uma retirada, o sistema consome primeiro o lote mais antigo.

Essa combinação organiza os produtos e seus diferentes lotes, respeitando a ordem de entrada. Uma única estrutura dificultaria separar a busca pelo produto do controle da ordem em que seus lotes devem ser consumidos.

### 3. Clientes e seus veículos

**Estruturas envolvidas:** `ListaEncadeada` e `Cliente.veiculos`.

Cada cliente pode possuir vários veículos, armazenados em uma lista encadeada. A busca por placa deve localizar o veículo e permitir identificar seu proprietário.

Essa combinação representa a relação entre um cliente e seus veículos sem estabelecer um limite fixo de veículos por cliente.

**Observação:** a integração entre a lista de veículos do cliente e o cadastro geral precisa ser conferida no código antes de considerar essa combinação concluída.

## Regras importantes

- Os veículos trazidos por guincho têm prioridade no atendimento.
- Os lotes devem ser consumidos do mais antigo para o mais recente.
- Lotes vencidos devem ser descartados e registrados como perdas.
- O sistema deve alertar quando o estoque ficar abaixo da quantidade mínima definida.
- A ordem de serviço só pode ser fechada após a conclusão da remontagem do veículo.
- O fechamento deve registrar o consumo das peças e o pagamento correspondente.

## Tecnologias e implementação

- Python.
- Estruturas de dados implementadas em classes próprias.
- Organização do código por responsabilidade.
- Controle de versões e entregas incrementais pelo GitHub.

## Status do projeto

Projeto acadêmico em desenvolvimento.
