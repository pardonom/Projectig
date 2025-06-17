import pytest
from Voting import Candidate, Ballot, OnlineVoter, InPersonVoter

@pytest.fixture
def setup_voting():
    c1 = Candidate("test candidate 1", "Party A")
    c2 = Candidate("test candidate 2", "Party B")
    ballot = Ballot()
    ballot.add_candidate(c1)
    ballot.add_candidate(c2)
    v1 = OnlineVoter("John", 1, "127.0.0.1")
    v2 = InPersonVoter("Jane", 2, "Booth 3")
    return c1, c2, ballot, v1, v2
    
def test_candidate_vote_count():
    c = Candidate("Alice", "Party X")
    c.receive_vote()
    assert c.votes == 1
    
def test_vote_count(setup_voting):
    c1, c2, ballot, v1, v2 = setup_voting
    v1.vote(ballot, c1, "2025-06-01")
    v2.vote(ballot, c2, "2025-06-01")
    assert c1.votes == 1
    assert c2.votes == 1