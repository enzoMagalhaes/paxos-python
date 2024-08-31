class Acceptor(object):

    messenger = None
    promised_id = None
    accepted_id = None
    accepted_value = None

    def recv_prepare(self, from_uid, proposal_id):
        """
        Called when a Prepare message is received from a Proposer
        """
        if proposal_id == self.promised_id:
            # Duplicate prepare message
            self.messenger.send_promise(
                from_uid, proposal_id, self.accepted_id, self.accepted_value
            )

        elif proposal_id > self.promised_id:
            self.promised_id = proposal_id
            self.messenger.send_promise(
                from_uid, proposal_id, self.accepted_id, self.accepted_value
            )

    def recv_accept_request(self, from_uid, proposal_id, value):
        """
        Called when an Accept! message is received from a Proposer
        """
        if proposal_id >= self.promised_id:
            self.promised_id = proposal_id
            self.accepted_id = proposal_id
            self.accepted_value = value
            self.messenger.send_accepted(proposal_id, self.accepted_value)
