import pytest

from openoligo.seq import Seq, is_valid_dna


def test_is_valid_dna():
    assert is_valid_dna("ATCG") == True
    assert is_valid_dna("ATCGatcg") == True
    assert is_valid_dna("ABCDE") == False
    assert is_valid_dna("") == True


def test_Seq_initialization():
    seq = Seq("ATCG")
    assert seq.seq == "ATCG"
    assert seq.index == 0

    with pytest.raises(ValueError):
        Seq("ABCDE")


def test_Seq_iter():
    seq = Seq("ATCG")
    assert iter(seq) == seq


def test_Seq_next():
    seq = Seq("ATCG")
    assert next(seq) == "A"
    assert next(seq) == "T"
    assert next(seq) == "C"
    assert next(seq) == "G"
    with pytest.raises(StopIteration):
        next(seq)


def test_Seq_repr():
    seq = Seq("ATCG")
    assert repr(seq) == "ATCG"


def test_Seq_len():
    seq = Seq("ATCG")
    assert len(seq) == 4


def test_Seq_getitem():
    seq = Seq("ATCG")
    assert seq[0] == "A"
    assert seq[1] == "T"
    assert seq[2] == "C"
    assert seq[3] == "G"
    with pytest.raises(IndexError):
        seq[4]
