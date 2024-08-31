from node import Node

# Set up nodes with their ports and neighbors
node1 = Node(1, 10001, {2: ('localhost', 10002), 3: ('localhost', 10003)})
node2 = Node(2, 10002, {1: ('localhost', 10001), 3: ('localhost', 10003)})
node3 = Node(3, 10003, {1: ('localhost', 10001), 2: ('localhost', 10002)})

node1.set_proposal("Value A")
node1.prepare()