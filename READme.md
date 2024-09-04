# Paxos Algorithm Implementation

Este projeto implementa um nó Paxos com comunicação por sockets. O algoritmo Paxos é utilizado para alcançar consenso em sistemas distribuídos. Cada nó pode atuar como um **Proposer**, **Acceptor** e **Learner**, comunicando-se com outros nós via sockets UDP.

## Estrutura do Projeto

O projeto é composto por três componentes principais, herdados pela classe `Node`:

- **Proposer**: Responsável por propor valores para consenso.
- **Acceptor**: Recebe e aceita propostas de consenso.
- **Learner**: Aprende o valor que foi aceito pela maioria dos Acceptors.

### Justificativa das Escolhas de Projeto

- **Uso de sockets**: A comunicação entre os nós ocorre de forma assíncrona via UDP sockets, o que reflete a natureza assíncrona de sistemas distribuídos reais. O UDP foi escolhido pela sua simplicidade e eficiência, uma vez que o Paxos é resiliente a perdas de mensagens.
- **Estrutura do Nó**: A classe `Node` herda as funções de Proposer, Acceptor e Learner para centralizar a lógica do Paxos em uma única entidade, facilitando a manutenção e escalabilidade do código. No entanto, isso requer um gerenciamento cuidadoso dos estados.
- **Mensagens em JSON**: O formato JSON foi escolhido pela sua simplicidade e compatibilidade universal para serialização de dados.

## Explicação Passo a Passo do Algoritmo

### Fase 1: Preparação
1. O **Proposer** escolhe um número de proposta único (geralmente crescente) e envia uma mensagem de `prepare` para um subconjunto de **Acceptors**.
2. Cada **Acceptor** verifica se o número da proposta é maior do que qualquer proposta anterior que ele tenha aceitado. Se for, o **Acceptor** envia uma `promise` ao **Proposer**, prometendo não aceitar propostas menores.

### Fase 2: Proposta
1. Após receber promessas de uma maioria (quórum) de **Acceptors**, o **Proposer** seleciona o valor da maior proposta aceita até então ou escolhe um novo valor se nenhuma proposta foi aceita.
2. O **Proposer** envia uma mensagem de `accept` para os **Acceptors**.
3. Se um **Acceptor** receber uma proposta válida (isto é, que seja maior do que qualquer outra que ele já tenha aceitado), ele aceita a proposta e envia uma confirmação ao **Proposer**.

### Fase 3: Decisão e Aprendizado
1. Quando uma maioria de **Acceptors** aceita a proposta, o valor é considerado aceito.
2. O **Learner** (que pode ser qualquer nó ou processo) é notificado do valor aceito e registra esse valor como o consenso final.

## Arquitetura

Cada nó mantém uma lista de vizinhos (outros nós participantes) com seus respectivos IPs e portas, e envia mensagens usando o formato JSON. As mensagens podem ser dos seguintes tipos:
- **prepare**: Proposta inicial de um Proposer.
- **promise**: Confirmação de um Acceptor de que ele não aceitará propostas menores.
- **accept**: Pedido para aceitar um valor proposto.
- **accepted**: Confirmação de que um valor foi aceito pela maioria.

### Diagrama UML

```mermaid
classDiagram
    class Proposer {
        +send_prepare(proposal_id)
        +send_promise(proposer_uid, proposal_id, previous_id, accepted_value)
    }

    class Acceptor {
        +recv_prepare(from_uid, proposal_id)
        +recv_promise(from_uid, proposal_id, prev_accepted_proposal, prev_accepted_value)
        +recv_accept_request(from_uid, proposal_id, value)
    }

    class Learner {
        +recv_accepted(from_uid, proposal_id, value)
        +on_resolution(proposal_id, value)
    }

    class Node {
        +send_message(target_uid, message_type, data)
        +receive_messages()
        +handle_message(message)
        +send_accept(proposal_id, proposal_value)
        +send_accepted(proposal_id, accepted_value)
    }

    Node --|> Proposer
    Node --|> Acceptor
    Node --|> Learner
```
### Execução

Como rodar?
- Clone o repositório.
- Crie os nós modificando os parâmetros de porta e IP, se necessário.
- Execute os nós simultaneamente para observar o processo de consenso.

Cada nó é criado com um identificador único, uma porta, e uma lista de vizinhos (UID, IP, porta). As mensagens são enviadas entre os nós para alcançar consenso. Exemplo para criação de nós:

```python
from node import Node

node1 = Node(1, 10001, {2: ('localhost', 10002), 3: ('localhost', 10003)})
node2 = Node(2, 10002, {1: ('localhost', 10001), 3: ('localhost', 10003)})
node3 = Node(3, 10003, {1: ('localhost', 10001), 2: ('localhost', 10002)})

node1.set_proposal("Value A")
node1.prepare()
```

Contribuição

Sinta-se à vontade para abrir issues ou enviar pull requests para melhorias ou correções.
