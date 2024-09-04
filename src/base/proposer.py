import collections

ProposalID = collections.namedtuple("ProposalID", ["number", "uid"])


class Proposer:

    proposed_value = None
    proposal_id = None
    last_accepted_id = None
    next_proposal_number = 1
    accepted_before_quorum = []

    def set_proposal(self, value):
        """
        Sets the proposal value for this node iff this node is not already aware of
        another proposal having already been accepted.
        """
        if self.proposed_value is None:
            self.proposed_value = value
            self.accepted_value = value

    def prepare(self):
        self.promises_rcvd = set()
        self.proposal_id = ProposalID(self.next_proposal_number, self.uid)

        self.next_proposal_number += 1

        self.messenger.send_prepare(self.proposal_id)

    def recv_promise(
        self, from_uid, proposal_id, prev_accepted_id, prev_accepted_value
    ):
        # Ignore the message if it's for an old proposal or we have already received
        # a response from this Acceptor
        if proposal_id != self.proposal_id or from_uid in self.promises_rcvd:
            return

        self.promises_rcvd.add(from_uid)

        if prev_accepted_id and prev_accepted_id > self.last_accepted_id:
            self.last_accepted_id = prev_accepted_id
            # If the Acceptor has already accepted a value, we MUST set our proposal
            # to that value.
            if prev_accepted_value is not None:
                self.proposed_value = prev_accepted_value


        if self.proposed_value is not None:
            if len(self.promises_rcvd) >= self.quorum_size-1:
                while self.accepted_before_quorum:
                    uid_b_quorum = self.accepted_before_quorum.pop()
                    self.messenger.send_accept(self.proposal_id, self.proposed_value, uid_b_quorum)
                self.messenger.send_accept(self.proposal_id, self.proposed_value, from_uid)
            else:
                self.accepted_before_quorum.append(from_uid)

