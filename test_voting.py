import pytest
from Voting import Voter, Candidate, Ballot, OnlineVoter, InPersonVoter

@pytest.fixture
def setup_voting():
    c1 = Candidate("Test Candidate 1", "Party A")
    c2 = Candidate("Test Candidate 2", "Party B")
    ballot = Ballot()
    ballot.add_candidate(c1)
    ballot.add_candidate(c2)
    v_online = OnlineVoter("John", 1, "192.168.0.2")
    v_inperson = InPersonVoter("Jane", 2, "Booth 3")
    return c1, c2, ballot, v_online, v_inperson

def test_voter_init(capsys):
    v = Voter("Alice", 99)
    captured = capsys.readouterr()
    assert "[born]" in captured.out
    assert "Alice" in captured.out
    assert not v._Voter__already_voted

def test_votes_kinds_init(setup_voting):
    _, _, _, v_online, v_inperson = setup_voting
    assert v_online.get_name() == "John"
    assert v_online.get_voter_id() == 1
    assert v_online._OnlineVoter__ip_address == "192.168.0.2"
    assert v_inperson.get_name() == "Jane"
    assert v_inperson.get_voter_id() == 2
    assert v_inperson._InPersonVoter__poll_booth == "Booth 3"

def test_candidate_init(setup_voting):
    c1, c2, _, _, _ = setup_voting
    assert c1.name == "Test Candidate 1"
    assert c1.party == "Party A"
    assert c1.votes == 0
    assert c2.name == "Test Candidate 2"
    assert c2.party == "Party B"
    assert c2.votes == 0

def test_ballot_init(capsys):
    b = Ballot()
    captured = capsys.readouterr()
    assert "[born b]" in captured.out
    assert len(b.candidates) == 0

def test_online_voter_ip_log(setup_voting, capsys):
    c1, _, ballot, v_online, _ = setup_voting
    v_online.vote(ballot, c1, "2025-06-01")
    captured = capsys.readouterr()
    assert "192.168.0.2" in captured.out
    assert "[vote o]" in captured.out

def test_inperson_voter_booth_log(setup_voting, capsys):
    _, c2, ballot, _, v_inperson = setup_voting
    v_inperson.vote(ballot, c2, "2025-06-01")
    captured = capsys.readouterr()
    assert "Booth 3" in captured.out
    assert "[vote p]" in captured.out
    
def test_candidate_receive_vote(setup_voting, capsys):
    c1, _, _, _, _ = setup_voting
    assert c1.votes == 0
    c1.receive_vote()
    captured = capsys.readouterr()
    assert c1.votes == 1
    assert "Test Candidate 1" in captured.out
    assert "Party A" in captured.out

def test_ballot_add_candidate(setup_voting, capsys):
    _, c2, ballot, _, _ = setup_voting
    captured = capsys.readouterr()
    ballot.add_candidate(c2)
    captured = capsys.readouterr()
    assert "[added to b]" in captured.out
    assert "Test Candidate 2" in captured.out

def test_ballot_record_vote_success(setup_voting, capsys):
    c1, _, ballot, _, _ = setup_voting
    ballot.record_vote(c1, "2025-06-01")
    captured = capsys.readouterr()
    assert "2025-06-01" in captured.out
    assert c1.votes == 1

def test_ballot_record_vote_fail(setup_voting, capsys):
    _, _, ballot, _, _ = setup_voting
    c3 = Candidate("Invalid", "Party X")
    ballot.record_vote(c3, "2025-06-01")
    captured = capsys.readouterr()
    assert "No such candidate exists" in captured.out

def test_voter_getters(setup_voting):
    _, _, _, v_online, v_inperson = setup_voting
    assert v_online.get_name() == "John"
    assert v_inperson.get_voter_id() == 2

def test_voter_vote_success(setup_voting, capsys):
    c1, _, ballot, _, v_inperson = setup_voting
    v_inperson.vote(ballot, c1, "2025-06-01")
    captured = capsys.readouterr()
    assert "Booth 3" in captured.out
    assert v_inperson._Voter__already_voted

def test_voter_vote_double(setup_voting, capsys):
    c1, _, ballot, v_online, v_inperson = setup_voting
    v_online.vote(ballot, c1, "2025-06-01")  
    capsys.readouterr()
    v_online.vote(ballot, c1, "2025-06-01") 
    captured = capsys.readouterr()
    assert "John" in captured.out
    assert "already voted" in captured.out
    v_inperson.vote(ballot, c1, "2025-06-01")  
    capsys.readouterr()
    v_inperson.vote(ballot, c1, "2025-06-01") 
    captured = capsys.readouterr()
    assert "Jane" in captured.out
    assert "already voted" in captured.out

def test_empty_ballot_vote(capsys):
    ballot = Ballot()
    v = Voter("Alice", 99)
    c = Candidate("Ghost", "Party Z")
    v.vote(ballot, c, "2025-06-01")
    captured = capsys.readouterr()
    assert "Ghost" in captured.out
    assert c.votes == 0

def test_voter_invalid_candidate(setup_voting, capsys):
    _, _, ballot, v_online, _ = setup_voting
    c3 = Candidate("Invalid", "Party X")
    v_online.vote(ballot, c3, "2025-06-01")
    captured = capsys.readouterr()
    assert "Invalid" in captured.out
    assert c3.votes == 0