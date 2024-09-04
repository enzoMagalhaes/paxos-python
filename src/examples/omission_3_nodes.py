import sys
import os

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from node import Node

quorum_size = 3
node1 = Node(
    1,
    10001,
    {
        2: ("localhost", 10002),
        3: ("localhost", 10003),
        4: ("localhost", 10004),
        5: ("localhost", 10005),
    },
    quorum_size
)
node2 = Node(
    2,
    10002,
    {
        1: ("localhost", 10001),
        3: ("localhost", 10003),
        4: ("localhost", 10004),
        5: ("localhost", 10005),
    },
    quorum_size,
    omission_limit=0
)
node3 = Node(
    3,
    10003,
    {
        1: ("localhost", 10001),
        2: ("localhost", 10002),
        4: ("localhost", 10004),
        5: ("localhost", 10005),
    },
    quorum_size,
    omission_limit=0
)
node4 = Node(
    4,
    10004,
    {
        1: ("localhost", 10001),
        2: ("localhost", 10002),
        3: ("localhost", 10003),
        5: ("localhost", 10005),
    },
    quorum_size,
    omission_limit=0
)
node5 = Node(
    5,
    10005,
    {
        1: ("localhost", 10001),
        2: ("localhost", 10002),
        3: ("localhost", 10003),
        4: ("localhost", 10004),
    },
    quorum_size,
)

node1.set_proposal("Value A")
node1.prepare()
