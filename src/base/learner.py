class Learner:

    proposals = {}  # maps proposal_id => [accept_count, retain_count, value]
    acceptors = {}  # maps from_uid => last_accepted_proposal_id
    final_value = None
    final_proposal_id = None

    @property
    def complete(self):
        return self.final_proposal_id is not None

    def recv_accepted(self, from_uid, proposal_id, accepted_value):
        """
        Called when an Accepted message is received from an acceptor
        """
        # print(f"final value: {self.final_value}")
        if self.final_value is not None:
            return  # already done

        last_pn = self.acceptors.get(from_uid)
        if last_pn and (not proposal_id >= last_pn):
            # print(f"old_msg {last_pn}")
            return  # Old message

        self.acceptors[from_uid] = proposal_id

        if last_pn is not None:
            oldp = self.proposals[last_pn]
            oldp[1] -= 1
            if oldp[1] == 0:
                del self.proposals[last_pn]

        if not proposal_id in self.proposals:
            self.proposals[proposal_id] = [0, 0, accepted_value]

        t = self.proposals[proposal_id]

        t[0] += 1
        t[1] += 1

        # print(t,self.quorum_size, self.accepted_value)

        if t[0] >= self.quorum_size or (t[0] == self.quorum_size-1 and self.accepted_value == t[2]):
            self.final_value = accepted_value
            self.final_proposal_id = proposal_id
            self.proposals = None
            self.acceptors = None

            self.messenger.on_resolution(proposal_id, accepted_value)
