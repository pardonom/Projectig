class Voter:
    def __init__(self, name, voter_id):
        self.__name = name
        self.__voter_id = voter_id
        self.__already_voted = False
        print(f"[born] Voter {self.__name}, id: {self.__voter_id}, has been registered.")

    def get_name(self):
        return self.__name

    def get_voter_id(self):
        return self.__voter_id


    def vote(self, voting_ballot, candidate, date):
        if self.__already_voted:
            print(f" Voter {self.__name}, has already voted.")

        else:
            voting_ballot.record_vote(candidate,date)
            self.__already_voted = True

    def __del__(self):
        print(f"[killed] Voter {self.__name}, has been removed from the system.")

class Candidate:
    def __init__(self, name, party):
        self.name=name
        self.party=party
        self.votes = 0
        print(f"[born c] Candidate: {self.name}, affiliated with party: {self.party}")


    def __del__(self):
        print(f"[killed c] Candidate {self.name} has been executed")

    def receive_vote(self):
        self.votes += 1
        print(f"[vote +]A vote has been recorded for {self.name} affiliated with {self.party}. They have now {self.votes} vote(s).")

class Ballot:
    def __init__(self):
        self.candidates = []

    def add_candidate(self, candidate):
        self.candidates.append(candidate)
        print(f"[added to b] Candidate {candidate.name} has been added to the ballot.")

    def record_vote(self, candidate, date):
        if candidate in self.candidates:
            print(f"[vote on record]A vote for {candidate.name} on {date} has been recorded.")
            candidate.receive_vote()
        else:
            print(f"[err] no such candidate exists")

    def __del__(self):
        print("[burned ballot] Ballot has been destroyed.")

class InPersonVoter(Voter):
    def __init__(self, name, voter_id, poll_booth):
        super().__init__(name, voter_id)
        self.__poll_booth = poll_booth

    def vote(self, voting_ballot, candidate, date):
        print(f"[vote b] Voting at booth {self.__poll_booth} on {date}")
        super().vote(voting_ballot, candidate, date)

    def __del__(self):
        print(f"[killed b] IRL voter {self.get_name()}, has been removed from the system.")


class OnlineVoter(Voter):
    def __init__(self, name, voter_id, ip_address):
        super().__init__(name, voter_id)
        self.__ip_address = ip_address

    def vote(self, voting_ballot, candidate, date):
        print(f"[vote o] Voting from ip: {self.__ip_address} on {date}")
        super().vote(voting_ballot, candidate, date)

    def __del__(self):
        print(f"[killed o] Online voter {self.get_name()}, has been removed from the system.")