import socket
import threading
import json

from base.proposer import Proposer, ProposalID
from base.acceptor import Acceptor
from base.learner import Learner

class Node(Proposer, Acceptor, Learner):
    """
    Implements a paxos node with a socket interface
    """
    def __init__(self, uid, port, neighbors, quorum_size, omission_limit = float('inf')):
        self.uid = uid
        self.port = port
        self.neighbors = neighbors  # A map of UID to (IP, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("localhost", port))
        self.messenger = self
        self.quorum_size = quorum_size  
        self.omission_limit = omission_limit
        self.message_counter = 0
        self.accepted_value = None
        threading.Thread(target=self.receive_messages).start()

    def send_message(self, target_uid, message_type, data):
        if self.message_counter < self.omission_limit:
            message = {
                "from_uid": self.uid,
                "type": message_type,
                "data": data
            }
            target_ip, target_port = self.neighbors[target_uid]
            self.sock.sendto(json.dumps(message).encode(), (target_ip, target_port))
            self.message_counter+=1

    def receive_messages(self):
        while self.message_counter < self.omission_limit:
            message, _ = self.sock.recvfrom(1024)
            message = json.loads(message.decode())
            print(f"{self.uid} recieved message {message}")
            self.handle_message(message)

    def handle_message(self, message):
        # Dispatch message based on type
        message_type = message['type']
        data = message['data']
        from_uid = message['from_uid']
        
        if message_type == 'prepare':
            self.recv_prepare(from_uid, ProposalID(**data))
        elif message_type == 'promise':
            prev_accepted_proposal = ProposalID(**data['prev_accepted_id']) if data['prev_accepted_id'] else None
            self.recv_promise(from_uid, ProposalID(**data['proposal_id']), 
                              prev_accepted_proposal, data['prev_accepted_value'])
        elif message_type == 'accept':
            self.recv_accept_request(from_uid, ProposalID(**data['proposal_id']), data['value'])
        elif message_type == 'accepted':
            self.recv_accepted(from_uid, ProposalID(**data['proposal_id']), data['value'])

    def send_prepare(self, proposal_id):
        for uid in self.neighbors:
            self.send_message(uid, 'prepare', proposal_id._asdict())

    def send_promise(self, proposer_uid, proposal_id, previous_id, accepted_value):
        self.send_message(proposer_uid, 'promise', {
            "proposal_id": proposal_id._asdict(),
            "prev_accepted_id": previous_id._asdict() if previous_id else None,
            "prev_accepted_value": accepted_value
        })

    def send_accept(self, proposal_id, proposal_value, from_uid):
        self.send_message(from_uid, 'accept', {
            "proposal_id": proposal_id._asdict(),
            "value": proposal_value
        })

    def send_accepted(self, proposal_id, accepted_value):
        for uid in self.neighbors:
            self.send_message(uid, 'accepted', {
                "proposal_id": proposal_id._asdict(),
                "value": accepted_value
            })

    def on_resolution(self, proposal_id, value):
        print(f"Node {self.uid} consensus value: {value}")
